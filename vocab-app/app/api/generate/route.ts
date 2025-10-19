import { NextResponse } from "next/server";
import { CohereClientV2 } from "cohere-ai";

const cohere = new CohereClientV2({
  token: process.env.COHERE_API_KEY || "",
});

export async function POST(req: Request) {
  try {
    const { category } = await req.json();

    if (!category || typeof category !== "string") {
      return NextResponse.json({ error: "Category is required." }, { status: 400 });
    }

    const prompt = `
You are a precise vocabulary generator from Korean to English.
Return STRICT JSON ONLY inside a single JSON code block.
Format: an array of vocabulary items.
Each item must include:
- "term": the Korean word or phrase
- "transliteration": Korean transliteration
- "translation": English meaning
- "parts": an array of objects, each with:
    - "part": syllable or segment
    - "transliteration": romanization
Generate 10 items maximum.
Thematic category to generate vocabulary for: "${category}".
`;

    const response = await cohere.chat({
      model: "command-a-03-2025",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.2,
      maxTokens: 2000,
    });

    // Get raw content
    let contentStr: string;
    const rawContent = response.message.content;

    if (Array.isArray(rawContent)) {
      contentStr = rawContent.map((c: any) => c?.text ?? "").join("\n");
    } else if (typeof rawContent === "string") {
      contentStr = rawContent;
    } else if (rawContent && typeof (rawContent as any).text === "string") {
      contentStr = (rawContent as any).text;
    } else {
      contentStr = String(rawContent ?? "");
    }

    // Remove markdown code block markers and trim
    const cleaned = contentStr.replace(/```json/i, "").replace(/```/g, "").trim();

    // Attempt normal JSON parse
    let vocabArray: any[] = [];
    try {
      vocabArray = JSON.parse(cleaned);
    } catch (err) {
      console.warn("AI returned incomplete JSON, attempting partial parse");

      // Try to extract only complete objects from array
      const objects = cleaned.match(/\{[^}]*\}/g);
      if (objects) {
        try {
          vocabArray = objects.map((obj) => JSON.parse(obj));
        } catch {
          console.error("Partial parse failed");
          return NextResponse.json(
            { error: "Failed to parse AI response as JSON." },
            { status: 500 }
          );
        }
      } else {
        return NextResponse.json(
          { error: "No valid JSON objects found in AI response." },
          { status: 500 }
        );
      }
    }

    return NextResponse.json({ vocab: vocabArray });
  } catch (err: any) {
    console.error("API error:", err);
    return NextResponse.json({ error: err?.message || "Internal error." }, { status: 500 });
  }
}
