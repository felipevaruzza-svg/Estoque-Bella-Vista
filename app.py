<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Estoque Chris Wellness Resort</title>

  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
      --brand-color: #868686;
      --brand-dark: #636363;
    }

    body {
      font-family: 'Inter', sans-serif;
      background: #fcfcfc;
      overscroll-behavior-y: none;
    }

    .glass-card {
      background: white;
      border: 1px solid #e5e7eb;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,.05);
    }

    .tab-active {
      border-bottom: 2px solid var(--brand-color);
      color: var(--brand-color);
    }

    .btn-primary {
      background: var(--brand-color);
    }

    .btn-primary:hover {
      background: var(--brand-dark);
    }

    .loading-overlay {
      position: fixed;
      inset: 0;
      background: white;
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    @media print {
      nav, header, button, .no-print, #stats-container, #toast,
      .modal-backdrop, #login-overlay { display: none !important; }
    }
  </style>
</head>

<body class="min-h-screen pb-12">

<!-- LOGIN -->
<div id="login-overlay" class="fixed inset-0 bg-slate-50 z-[2000] flex items-center justify-center">
  <div class="bg-white p-8 rounded-3xl shadow-xl w-full max-w-sm text-center">
    <h2 class="text-2xl font-bold mb-4">Acesso ao Estoque</h2>
    <input id="access-pass" type="password" placeholder="Código de Acesso"
      class="w-full px-4 py-3 border rounded-xl text-center mb-4">
    <button onclick="checkAccess()" class="btn-primary text-white w-full py-3 rounded-xl font-bold">
      Entrar
    </button>
    <p id="access-error" class="hidden text-red-500 text-sm mt-3">Código incorreto</p>
  </div>
</div>

<!-- LOADING -->
<div id="loading-screen" class="loading-overlay hidden">
  <div class="animate-spin rounded-full h-10 w-10 border-4 border-slate-300 border-t-slate-800"></div>
</div>

<!-- APP -->
<div id="main-content" class="hidden max-w-6xl mx-auto px-4 py-8">

  <header class="flex justify-between items-center mb-8">
    <h1 class="text-xl font-black">Chris Wellness Resort</h1>
    <button onclick="openNewTransaction()" class="btn-primary text-white px-6 py-3 rounded-xl font-bold">
      <i class="fas fa-plus mr-2"></i>Novo Registro
    </button>
  </header>

  <div id="stats-container" class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6"></div>

  <div class="flex gap-6 mb-6 border-b">
    <button id="tab-history" onclick="switchTab('history')" class="tab-active pb-3 font-bold">
      Movimentações
    </button>
    <button id="tab-report" onclick="switchTab('report')" class="pb-3 font-bold text-slate-400">
      Relatório
    </button>
  </div>

  <div id="view-history" class="glass-card rounded-xl overflow-hidden">
    <div class="p-4 border-b">
      <input id="search-input" oninput="renderData()" placeholder="Buscar item..."
        class="px-4 py-2 border rounded-xl w-full sm:w-64">
    </div>
    <table class="w-full text-sm">
      <thead class="bg-slate-50 text-slate-400 text-xs uppercase">
        <tr>
          <th class="px-4 py-3">Data</th>
          <th class="px-4 py-3">Item</th>
          <th class="px-4 py-3">Setor</th>
          <th class="px-4 py-3">Qtd</th>
          <th class="px-4 py-3 text-right">Ações</th>
        </tr>
      </thead>
      <tbody id="inventory-body"></tbody>
    </table>
  </div>

  <div id="view-report" class="hidden glass-card rounded-xl overflow-hidden">
    <table class="w-full text-sm">
      <thead class="bg-slate-50 text-slate-400 text-xs uppercase">
        <tr>
          <th class="px-4 py-3">Produto</th>
          <th class="px-4 py-3">Entradas</th>
          <th class="px-4 py-3">Saídas</th>
          <th class="px-4 py-3">Saldo</th>
        </tr>
      </thead>
      <tbody id="report-body"></tbody>
    </table>
  </div>

</div>

<!-- TOAST -->
<div id="toast"
 class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-slate-900 text-white px-6 py-3 rounded-xl opacity-0 transition">
</div>

<!-- SCRIPT -->
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
  import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
  import {
    getFirestore, collection, addDoc, deleteDoc,
    onSnapshot, doc, setDoc
  } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

  /* 🔥 SUBSTITUA PELOS SEUS DADOS */
  const firebaseConfig = {
    apiKey: "SUA_API_KEY",
    authDomain: "SEU_PROJETO.firebaseapp.com",
    projectId: "SEU_PROJETO",
    storageBucket: "SEU_PROJETO.appspot.com",
    messagingSenderId: "XXXX",
    appId: "1:XXXX:web:XXXX"
  };

  const ACCESS_PASS = "Hotel303021";
  const appId = "chris-wellness-estoque";

  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const db = getFirestore(app);

  let inventory = [];
  let currentTab = "history";

  window.checkAccess = async () => {
    if (access-pass.value === ACCESS_PASS) {
      login-overlay.style.display = "none";
      main-content.classList.remove("hidden");
      loading-screen.classList.remove("hidden");
      await signInAnonymously(auth);
    } else access-error.classList.remove("hidden");
  };

  onAuthStateChanged(auth, user => {
    if (!user) return;
    onSnapshot(collection(db, "artifacts", appId, "public", "data", "inventory"), snap => {
      inventory = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderData();
      loading-screen.classList.add("hidden");
    });
  });

  window.switchTab = tab => {
    currentTab = tab;
    view-history.classList.toggle("hidden", tab !== "history");
    view-report.classList.toggle("hidden", tab !== "report");
    tab-history.classList.toggle("tab-active", tab === "history");
    tab-report.classList.toggle("tab-active", tab === "report");
    renderData();
  };

  window.renderData = () => {
    if (currentTab === "history") {
      inventory-body.innerHTML = inventory.map(i => `
        <tr>
          <td class="px-4 py-2">${i.date}</td>
          <td class="px-4 py-2 font-bold">${i.name}</td>
          <td class="px-4 py-2">${i.category}</td>
          <td class="px-4 py-2">${i.qty}</td>
          <td class="px-4 py-2 text-right">
            <button onclick="deleteItem('${i.id}')" class="text-red-500">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
      `).join("");
    } else {
      const map = {};
      inventory.forEach(i => {
        if (!map[i.name]) map[i.name] = { in: 0, out: 0 };
        i.type === "entrada" ? map[i.name].in += +i.qty : map[i.name].out += +i.qty;
      });
      report-body.innerHTML = Object.keys(map).map(n => `
        <tr>
          <td class="px-4 py-2 font-bold">${n}</td>
          <td class="px-4 py-2 text-emerald-600">+${map[n].in}</td>
          <td class="px-4 py-2 text-orange-500">-${map[n].out}</td>
          <td class="px-4 py-2 font-black">${map[n].in - map[n].out}</td>
        </tr>
      `).join("");
    }
  };

  window.deleteItem = async id => {
    await deleteDoc(doc(db, "artifacts", appId, "public", "data", "inventory", id));
  };
</script>

</body>
</html>
