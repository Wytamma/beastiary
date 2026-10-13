export const getLocalToken = () => localStorage.getItem("token");

export const saveLocalToken = (token: string) =>
  localStorage.setItem("token", token);

export const removeLocalToken = () => localStorage.removeItem("token");

// Keep every `interval`-th sample: for interval k = 5 the 5th, 10th, 15th, ... are kept and the rest dropped.
// An interval of 1 keeps everything. If the interval is longer than the data nothing would survive, so the input is
// returned unchanged rather than leaving an empty plot. Equal-length inputs thin identically, so parallel arrays
// stay aligned.
export function thin<T>(rows: T[], interval: number): T[] {
  if (!(interval > 1) || rows.length < interval) {
    return rows;
  }
  return rows.filter((_, index) => (index + 1) % interval === 0);
}
