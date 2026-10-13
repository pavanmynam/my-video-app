export default async function handler(req, res) {
  const prompt = req.query.prompt || "a cute cat";
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt + " realistic motion, 8k, cinematic, ultra detailed")}?width=1280&height=720&seed=${Date.now()}&nologo=true&model=turbo`;
  res.json({ video: url });
}
