import { thin } from "@/utils";

const range = (n: number) => Array.from({ length: n }, (_, i) => i);

describe("thin", () => {
  it("returns the input untouched for an interval of 1", () => {
    const rows = range(100);
    expect(thin(rows, 1)).toBe(rows);
  });

  it("keeps samples k, 2k, 3k, ... (1-indexed) and drops the rest", () => {
    // k = 5 over samples 1..20 keeps samples 5, 10, 15, 20, i.e. indices 4, 9, 14, 19.
    expect(thin(range(20), 5)).toEqual([4, 9, 14, 19]);
    expect(thin(range(10), 5)).toEqual([4, 9]);
    expect(thin(range(10), 2)).toEqual([1, 3, 5, 7, 9]);
  });

  it("drops a trailing partial block", () => {
    expect(thin(range(12), 5)).toEqual([4, 9]);
  });

  it("returns the input unchanged when the interval exceeds the number of samples", () => {
    const rows = range(4);
    expect(thin(rows, 5)).toBe(rows);
    expect(thin(rows, 1000)).toBe(rows);
  });

  it("keeps the last sample when the interval equals the number of samples", () => {
    expect(thin(range(5), 5)).toEqual([4]);
  });

  it("ignores invalid intervals", () => {
    const rows = range(10);
    expect(thin(rows, 0)).toBe(rows);
    expect(thin(rows, -3)).toBe(rows);
    expect(thin(rows, NaN)).toBe(rows);
  });

  it("keeps equal-length arrays aligned", () => {
    const states = range(1000);
    const values = states.map((s) => s * 2);
    expect(thin(values, 7)).toEqual(thin(states, 7).map((s) => s * 2));
  });

  it("does not mutate its input", () => {
    const rows = range(10);
    thin(rows, 3);
    expect(rows).toEqual(range(10));
  });
});
