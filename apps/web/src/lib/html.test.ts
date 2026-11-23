import { describe, expect, it } from "vitest";

import { htmlToLines } from "./html";

describe("htmlToLines", () => {
  it("removes tags and empty lines", () => {
    const html = '<b>📉 Price drop: -12%</b>\n<a href="https://a.test">Kindle</a>\n\nNow: <b>$89</b>';

    expect(htmlToLines(html)).toEqual(["📉 Price drop: -12%", "Kindle", "Now: $89"]);
  });

  it("decodes escaped characters once", () => {
    expect(htmlToLines("Mouse &lt;Pro&gt; &amp;amp; more")).toEqual(["Mouse <Pro> &amp; more"]);
  });
});
