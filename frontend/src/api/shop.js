export async function askShop(topic) {
  const res = await fetch("http://127.0.0.1:8002/shop", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });
  if (!res.ok) throw new Error("Backend failed");
  return await res.json();
}