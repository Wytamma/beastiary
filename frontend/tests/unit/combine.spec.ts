import {
  COMBINED_TRACE_ID,
  combineThinningInterval,
  combineTraces,
  CombineSettings,
  withActiveParams,
} from "@/combine";
import { Trace } from "@/interfaces";
import Vue from "vue";

const AUTO: CombineSettings = {
  combineMode: "all",
  combineThinning: "auto",
  combineThinningInterval: 2,
};

// Every parameter's values encode which trace and which sample they came from: id * 100000 + sample index.
function makeTrace(
  id: number,
  path: string,
  length: number,
  overrides: Partial<Trace> = {},
  params: string[] = ["a"],
): Trace {
  const indices = Array.from({ length }, (_, i) => i);
  const parameters: Trace["parameters"] = {
    state: indices.map((i) => ({ state: i * 1000, value: i * 1000 })),
  };
  for (const param of params) {
    parameters[param] = indices.map((i) => ({
      state: i * 1000,
      value: id * 100000 + i,
    }));
  }
  return {
    id,
    path,
    headers_line: "",
    delimiter: "",
    last_byte: 0,
    source: "local",
    parameters,
    activeParams: ["a"],
    isActive: true,
    burnIn: 0,
    isLoading: false,
    ...overrides,
  };
}

describe("combineTraces grouping", () => {
  it("combines a parameter two traces have, whatever the traces are called", () => {
    const combined = combineTraces(
      [makeTrace(1, "/runs/1/one.log", 10), makeTrace(2, "two.log", 10)],
      AUTO,
    );
    expect(combined).toHaveLength(1);
    expect(combined[0].source).toBe("combined");
    expect(combined[0].id).toBe(COMBINED_TRACE_ID);
    expect(Object.keys(combined[0].parameters)).toEqual(["state", "a"]);
    expect(combined[0].combined!.memberIDs).toEqual([1, 2]);
    expect(combined[0].combined!.parameters.a.memberIDs).toEqual([1, 2]);
  });

  it("does not combine different traces' parameters with different names", () => {
    const traces = [
      makeTrace(1, "a.log", 10, {}, ["a"]),
      makeTrace(2, "a.log", 10, {}, ["b"]),
    ];
    expect(combineTraces(traces, AUTO)).toEqual([]);
  });

  it("does not combine a parameter only one trace has", () => {
    expect(combineTraces([makeTrace(1, "a.log", 10)], AUTO)).toEqual([]);
  });

  it("combines every parameter two or more loaded traces have, selected or not", () => {
    const traces = [
      makeTrace(1, "a.log", 10, { activeParams: [] }, ["joint", "x"]),
      makeTrace(2, "b.log", 10, { activeParams: [] }, ["joint", "y"]),
      makeTrace(3, "c.log", 10, { activeParams: [] }, ["joint", "x"]),
      makeTrace(4, "d.log", 10, { parameters: {} }, ["joint"]), // samples not loaded yet
    ];
    const [combined] = combineTraces(traces, AUTO);
    expect(Object.keys(combined.parameters)).toEqual(["state", "joint", "x"]);
    expect(combined.combined!.parameters.joint.memberIDs).toEqual([1, 2, 3]);
    expect(combined.combined!.parameters.x.memberIDs).toEqual([1, 3]);
    expect(combined.combined!.memberIDs).toEqual([1, 2, 3]);
    // Each parameter is thinned by the number of traces it combines.
    expect(combined.combined!.parameters.joint.thinning).toBe(3);
    expect(combined.combined!.parameters.x.thinning).toBe(2);
    // y is only in one trace and nothing is selected on the combined trace.
    expect(combined.activeParams).toEqual([]);
  });

  it("does nothing when combining is off", () => {
    const traces = [makeTrace(1, "a.log", 10), makeTrace(2, "b.log", 10)];
    expect(combineTraces(traces, { ...AUTO, combineMode: "off" })).toEqual([]);
  });

  it("ignores combined traces passed back in", () => {
    const traces = [makeTrace(1, "a.log", 10), makeTrace(2, "b.log", 10)];
    const first = combineTraces(traces, AUTO);
    const again = combineTraces([...traces, ...first], AUTO);
    expect(again).toHaveLength(1);
    expect(again[0].combined!.memberIDs).toEqual([1, 2]);
  });

  it("keeps the parameters selected on the combined trace that still exist", () => {
    const traces = [
      makeTrace(1, "a.log", 10, { activeParams: ["a", "x"] }, ["a", "x"]),
      makeTrace(2, "b.log", 10, { activeParams: ["a", "x"] }, ["a", "x"]),
    ];
    const [base] = combineTraces(traces, AUTO);
    const combined = withActiveParams(base, ["x", "gone"]);
    expect(combined.activeParams).toEqual(["x"]);
    expect(base.activeParams).toEqual([]);
  });

  it("selecting parameters reuses the combined data instead of rebuilding it", () => {
    const traces = [
      makeTrace(1, "a.log", 100, {}, ["a", "x"]),
      makeTrace(2, "b.log", 100, {}, ["a", "x"]),
    ];
    const [base] = combineTraces(traces, AUTO);
    const rows = base.parameters.a;
    const state = base.parameters.state;
    const selected = withActiveParams(base, ["a"]);
    expect(selected.activeParams).toEqual(["a"]);
    expect(selected.parameters.a).toBe(rows);
    expect(selected.parameters.state).toBe(state);
    const deselected = withActiveParams(selected, []);
    expect(deselected.activeParams).toEqual([]);
    expect(deselected.parameters.a).toBe(rows);
    // Nothing to change: the same trace comes back.
    expect(withActiveParams(base, [])).toBe(base);
  });
});

describe("combineTraces thinning", () => {
  const twoTraces = () => [
    makeTrace(1, "a.log", 100),
    makeTrace(2, "b.log", 100),
  ];

  it("defaults to k = the number of traces, so the combined parameter is as long as one trace's", () => {
    const [combined] = combineTraces(twoTraces(), AUTO);
    expect(combined.combined!.parameters.a.thinning).toBe(2);
    expect(combined.parameters.a).toHaveLength(100);
    expect(combined.parameters.state).toHaveLength(100);
  });

  it("uses k = 3 for three traces", () => {
    const traces = [...twoTraces(), makeTrace(3, "c.log", 99)];
    const [combined] = combineTraces(traces, AUTO);
    expect(combined.combined!.parameters.a.thinning).toBe(3);
    // floor(100 / 3) + floor(100 / 3) + floor(99 / 3)
    expect(combined.parameters.a).toHaveLength(33 + 33 + 33);
  });

  it("thins each trace separately, keeping samples k, 2k, 3k, ...", () => {
    const [combined] = combineTraces(twoTraces(), AUTO);
    const values = combined.parameters.a.map((row) => row.value as number);
    // Trace 1 contributes its samples at (0-based) indices 1, 3, 5, ... then trace 2 does.
    expect(values.slice(0, 3)).toEqual([100001, 100003, 100005]);
    expect(values.slice(50, 53)).toEqual([200001, 200003, 200005]);
    expect(values.filter((v) => v < 200000)).toHaveLength(50);
  });

  it("applies each trace's burn-in before thinning, like LogCombiner", () => {
    const traces = [
      makeTrace(1, "a.log", 100, { burnIn: 50 }),
      makeTrace(2, "b.log", 100, { burnIn: 0 }),
    ];
    const [combined] = combineTraces(traces, AUTO);
    const values = combined.parameters.a.map((row) => row.value as number);
    // Trace 1: samples 50..99 thinned by 2 -> indices 51, 53, ..., 99 (25 samples).
    expect(values[0]).toBe(100051);
    expect(values.filter((v) => v < 200000)).toHaveLength(25);
    expect(values.filter((v) => v > 200000)).toHaveLength(50);
    // The combined trace has no burn-in of its own, so plots don't remove samples a second time.
    expect(combined.burnIn).toBe(0);
  });

  it("can be switched off to keep every sample", () => {
    const [combined] = combineTraces(twoTraces(), {
      ...AUTO,
      combineThinning: "off",
    });
    expect(combined.combined!.parameters.a.thinning).toBe(1);
    expect(combined.parameters.a).toHaveLength(200);
  });

  it("can use a custom interval", () => {
    const [combined] = combineTraces(twoTraces(), {
      ...AUTO,
      combineThinning: "custom",
      combineThinningInterval: 10,
    });
    expect(combined.combined!.parameters.a.thinning).toBe(10);
    expect(combined.parameters.a).toHaveLength(20);
  });

  it("picks the interval from the settings", () => {
    expect(combineThinningInterval(AUTO, 4)).toBe(4);
    expect(
      combineThinningInterval({ ...AUTO, combineThinning: "off" }, 4),
    ).toBe(1);
    expect(
      combineThinningInterval(
        { ...AUTO, combineThinning: "custom", combineThinningInterval: 7 },
        4,
      ),
    ).toBe(7);
  });

  it("thins parameters combined from different numbers of traces by different amounts", () => {
    const traces = [
      makeTrace(1, "a.log", 100, {}, ["a", "x"]),
      makeTrace(2, "b.log", 100, {}, ["a", "x"]),
      makeTrace(3, "c.log", 100, {}, ["a"]),
    ];
    const [combined] = combineTraces(traces, AUTO);
    expect(combined.parameters.a).toHaveLength(33 * 3);
    expect(combined.parameters.x).toHaveLength(50 * 2);
    // `state` follows the longest parameter.
    expect(combined.parameters.state).toHaveLength(100);
  });

  it("keeps each parameter's state increasing across the joins between traces", () => {
    const [combined] = combineTraces(twoTraces(), AUTO);
    const states = combined.parameters.a.map((row) => row.state);
    for (let i = 1; i < states.length; i++) {
      expect(states[i]).toBeGreaterThan(states[i - 1]);
    }
    // Thinned by 2 so consecutive samples are 2000 apart.
    expect(states[1] - states[0]).toBe(2000);
    expect(states[states.length - 1]).toBe(100 * 2000);
    expect(combined.parameters.state.map((row) => row.state)).toEqual(states);
  });
});

describe("combined trace data", () => {
  it("returns the same arrays until something changes", () => {
    const [combined] = combineTraces(
      [makeTrace(1, "a.log", 100), makeTrace(2, "b.log", 100)],
      AUTO,
    );
    expect(combined.parameters.a).toBe(combined.parameters.a);
    expect(combined.parameters.state).toBe(combined.parameters.state);
  });

  it("does not modify the member traces", () => {
    const traces = [makeTrace(1, "a.log", 20), makeTrace(2, "b.log", 20)];
    combineTraces(traces, AUTO)[0].parameters.a;
    expect(traces[0].parameters.a).toHaveLength(20);
    expect(traces[1].parameters.a).toHaveLength(20);
  });

  it("reports loading while a member is loading", () => {
    const traces = [
      makeTrace(1, "a.log", 10),
      makeTrace(2, "b.log", 10, { isLoading: true }),
    ];
    expect(combineTraces(traces, AUTO)[0].isLoading).toBe(true);
  });

  it("is frozen so deep watchers don't build every parameter", () => {
    const [combined] = combineTraces(
      [makeTrace(1, "a.log", 10), makeTrace(2, "b.log", 10)],
      AUTO,
    );
    expect(Object.isFrozen(combined.parameters)).toBe(true);
  });

  // The store builds the combined trace in a getter (a Vue computed), so it is rebuilt when a member changes.
  describe("reactivity", () => {
    const setup = () => {
      const members = Vue.observable({
        list: [makeTrace(1, "a.log", 10), makeTrace(2, "b.log", 10)],
      }).list;
      const getter = new Vue({
        computed: {
          combined: () =>
            combineTraces(members, { ...AUTO, combineThinning: "off" })[0],
        },
      });
      const reader = () =>
        new Vue({
          computed: { value: () => (getter as any).combined.parameters.a.length },
        });
      // Adding samples replaces every parameter's array, `state` included.
      const addSample = (member: Trace) => {
        member.parameters.state = member.parameters.state.concat([
          { state: 10000, value: 10000 },
        ]);
        member.parameters.a = member.parameters.a.concat([
          { state: 10000, value: 1 },
        ]);
      };
      return { members, reader, addSample };
    };

    it("updates readers when a member trace gets more samples", () => {
      const { members, reader, addSample } = setup();
      const length = reader();
      expect(length.value).toBe(20);
      addSample(members[0]);
      expect(length.value).toBe(21);
    });

    it("updates every reader, including ones that read the cached data", () => {
      const { members, reader, addSample } = setup();
      const first = reader();
      const second = reader();
      expect(first.value).toBe(20);
      expect(second.value).toBe(20);
      addSample(members[1]);
      expect(first.value).toBe(21);
      expect(second.value).toBe(21);
    });

    it("updates readers when a member's burn-in changes", () => {
      const { members, reader } = setup();
      const length = reader();
      expect(length.value).toBe(20);
      members[0].burnIn = 50;
      expect(length.value).toBe(15);
    });

    it("doesn't read the members again when the combined data is read again", () => {
      const traces = [makeTrace(1, "a.log", 10), makeTrace(2, "b.log", 10)];
      let reads = 0;
      for (const trace of traces) {
        const rows = trace.parameters.a;
        Object.defineProperty(trace.parameters, "a", {
          enumerable: true,
          get: () => {
            reads++;
            return rows;
          },
        });
      }
      const [combined] = combineTraces(traces, AUTO);
      combined.parameters.a;
      const readsToBuild = reads;
      expect(readsToBuild).toBeGreaterThan(0);
      for (let i = 0; i < 5; i++) {
        combined.parameters.a;
        combined.parameters.state;
      }
      expect(reads).toBe(readsToBuild);
    });
  });
});
