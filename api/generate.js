export default async function handler(req, res) {
  const prompt = req.query.prompt || "a cute cat";
  const HF_TOKEN = process.env.HF_TOKEN;

  if (!HF_TOKEN) {
    return res.status(500).json({ error: "HF_TOKEN ledu bro - Vercel lo add chey" });
  }

  try {
    // FREE model - FLUX - super realistic
    const response = await fetch("https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${HF_TOKEN}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 
        inputs: prompt + ", realistic, ultra detailed, 8k, cinematic, photorealistic",
        parameters: { guidance_scale: 7.5 }
      })
    });

    if (!response.ok) {
      // Model busy aithe fallback
      const fallback = `https://picsum.photos/seed/${Date.now()}/1280/720`;
      return res.json({ video: fallback, note: "Model loading, retry after 10 sec" });
    }

    const arrayBuffer = await response.arrayBuffer();
    const base64 = Buffer.from(arrayBuffer).toString('base64');
    const imageUrl = `data:image/jpeg;base64,${base64}`;
    
    res.json({ video: imageUrl });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
