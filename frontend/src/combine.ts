import { Data, Trace } from "@/interfaces";
import { SettingsState } from "@/store/settings/state";
import { thin } from "@/utils";

export type CombineSettings = Pick<
  SettingsState,
  "combineMode" | "combineThinning" | "combineThinningInterval"
>;

// Local traces count down from -1, so the combined trace gets an ID far away from those.
export const COMBINED_TRACE_ID = -1000000000;
export const COMBINED_TRACE_NAME = "Combined";

// The thinning interval applied to each of `count` traces before their parameter is combined.
export function combineThinningInterval(
  settings: CombineSettings,
  count: number,
): number {
  switch (settings.combineThinning) {
    case "off":
      return 1;
    case "custom":
      return settings.combineThinningInterval;
    default:
      return count;
  }
}

function hasSamples(trace: Trace) {
  return (
    !!trace.parameters &&
    !!trace.parameters.state &&
    trace.parameters.state.length > 0
  );
}

// A member's rows for one parameter once its burn-in is removed and it is thinned.
function memberRows(member: Trace, param: string, interval: number): Data[] {
  const start = Math.floor(
    (member.parameters.state.length * member.burnIn) / 100,
  );
  return thin(member.parameters[param].slice(start), interval);
}

interface ParameterGroup {
  param: string;
  members: Trace[];
  interval: number;
}

// Combine parameters that have the same name in different traces into one synthetic "combined" trace.
//
// - A parameter is combined when at least two loaded traces have it, whether or not it is selected in them. Nothing is
//   combined when the combine mode is 'off'.
// - Like BEAST's LogCombiner, each trace has its own burn-in removed (the burn-in set on that trace), is thinned to
//   every k-th sample, and the results are concatenated. Thinning each trace (rather than the concatenation) keeps the
//   traces equally represented. Because this happens when the combined trace is built, ESS and statistics see the
//   thinned samples.
// - `state` counts the samples up (each trace advances it by its own thinned step) so it is increasing across the
//   joins. The combined trace's own burn-in is 0 because the traces' burn-ins have already been applied.
// - Parameters are built lazily, the first time they are read, since a trace can have hundreds of them. Reading one
//   always reads the member traces too so whatever is reading it stays reactive to changes in them.
//
// Returns an empty array when nothing can be combined.
export function combineTraces(
  traces: Trace[],
  settings: CombineSettings,
  activeParams: string[] = [],
): Trace[] {
  if (settings.combineMode === "off") {
    return [];
  }

  const byParam = new Map<string, Trace[]>();
  for (const trace of traces) {
    if (trace.source === "combined" || !hasSamples(trace)) {
      continue;
    }
    for (const param of Object.keys(trace.parameters)) {
      if (param === "state") {
        continue;
      }
      const members = byParam.get(param);
      if (!members) {
        byParam.set(param, [trace]);
      } else if (members[members.length - 1] !== trace) {
        members.push(trace);
      }
    }
  }

  const groups: ParameterGroup[] = [];
  byParam.forEach((members, param) => {
    if (members.length >= 2) {
      groups.push({
        param,
        members,
        interval: combineThinningInterval(settings, members.length),
      });
    }
  });
  if (groups.length === 0) {
    return [];
  }
  return [makeCombinedTrace(groups, activeParams)];
}

function makeCombinedTrace(
  groups: ParameterGroup[],
  activeParams: string[],
): Trace {
  const cache = new Map<string, { inputs: unknown[]; result: any }>();
  const cached = <T>(key: string, inputs: unknown[], build: () => T): T => {
    const hit = cache.get(key);
    if (
      hit &&
      hit.inputs.length === inputs.length &&
      hit.inputs.every((input, i) => input === inputs[i])
    ) {
      return hit.result;
    }
    const result = build();
    cache.set(key, { inputs, result });
    return result;
  };

  const groupByParam = new Map<string, ParameterGroup>();
  groups.forEach((group) => groupByParam.set(group.param, group));

  const memberIDs: number[] = [];
  const info: NonNullable<Trace["combined"]>["parameters"] = {};
  for (const group of groups) {
    info[group.param] = {
      memberIDs: group.members.map((member) => member.id),
      thinning: group.interval,
    };
    for (const member of group.members) {
      if (memberIDs.indexOf(member.id) === -1) {
        memberIDs.push(member.id);
      }
    }
  }

  // The combined state counter for a set of traces. Many parameters share the same set, so it is built once per set.
  // Reading it registers the traces' state arrays and burn-ins as dependencies of the reader.
  const axisKey = (group: ParameterGroup) =>
    `${group.interval}:${group.members.map((member) => member.id).join(",")}`;
  const axis = (group: ParameterGroup): number[] =>
    cached(
      `axis:${axisKey(group)}`,
      [
        ...group.members.map((member) => member.parameters.state),
        ...group.members.map((member) => member.burnIn),
      ],
      () => {
        const values: number[] = [];
        let counter = 0;
        for (const member of group.members) {
          const rows = memberRows(member, "state", group.interval);
          const step =
            rows.length > 1 && rows[1].state > rows[0].state
              ? rows[1].state - rows[0].state
              : 1;
          for (let i = 0; i < rows.length; i++) {
            counter += step;
            values.push(counter);
          }
        }
        return values;
      },
    );

  // `state` is the longest of the parameters' counters.
  const stateRows = (): Data[] => {
    let longest: number[] = [];
    groups.forEach((group) => {
      const states = axis(group);
      if (states.length > longest.length) {
        longest = states;
      }
    });
    return cached(
      "state-rows",
      [longest],
      () =>
        Object.freeze(
          longest.map((state) => ({ state, value: state })),
        ) as Data[],
    );
  };

  const parameterRows = (group: ParameterGroup): Data[] => {
    const states = axis(group);
    const inputs = [
      states,
      ...group.members.map((member) => member.parameters[group.param]),
    ];
    return cached(`param:${group.param}`, inputs, () => {
      const rows: Data[] = [];
      for (const member of group.members) {
        for (const row of memberRows(member, group.param, group.interval)) {
          const index = rows.length;
          rows.push({
            state: index < states.length ? states[index] : index + 1,
            value: row.value,
          });
        }
      }
      return Object.freeze(rows) as Data[];
    });
  };

  const parameters = {} as Trace["parameters"];
  Object.defineProperty(parameters, "state", {
    enumerable: true,
    get: stateRows,
  });
  for (const group of groups) {
    Object.defineProperty(parameters, group.param, {
      enumerable: true,
      get: () => parameterRows(group),
    });
  }
  // Frozen so Vue's deep watchers don't walk it (which would build every parameter).
  Object.freeze(parameters);

  return {
    id: COMBINED_TRACE_ID,
    path: `${COMBINED_TRACE_NAME} parameters`,
    headers_line: "",
    delimiter: "",
    last_byte: 0,
    source: "combined",
    parameters,
    activeParams: activeParams.filter((param) => groupByParam.has(param)),
    isActive: true,
    burnIn: 0,
    isLoading: groups.some((group) =>
      group.members.some((member) => member.isLoading),
    ),
    combined: { memberIDs, parameters: info },
  };
}
