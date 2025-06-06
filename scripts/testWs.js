const { WebSocket } = require('ws');

const ws = new WebSocket('wss://stylish-red-wildflower.base-mainnet.quiknode.pro/d2df1554392e6deea8124dc6a19434b49bf0a53b/');

ws.on('open', () => {
  console.log('🔗 Connected to QuickNode WebSocket');

  ws.send(JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "eth_subscribe",
    params: ["newPendingTransactions"]
  }));
});

ws.on('message', (data) => {
  const parsed = JSON.parse(data.toString());
  if (parsed.method === 'eth_subscription' && parsed.params?.result) {
    console.log('📦 Pending TX Hash:', parsed.params.result);
  } else {
    console.log('[DEBUG] Message:', parsed);
  }
});

ws.on('error', (err) => {
  console.error('❌ WebSocket Error:', err);
});
