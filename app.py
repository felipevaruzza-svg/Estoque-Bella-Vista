<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estoque Chris Wellness Resort Hotel</title>
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
            background-color: #fcfcfc;
            /* Previne o bounce effect no iOS */
            overscroll-behavior-y: none;
        }
        
        .glass-card {
            background: white;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .tab-active {
            border-bottom: 2px solid var(--brand-color);
            color: var(--brand-color);
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

        .btn-primary {
            background-color: var(--brand-color);
            transition: all 0.2s;
        }
        .btn-primary:hover {
            background-color: var(--brand-dark);
            transform: translateY(-1px);
        }

        @media print {
            nav, header, button, .no-print, #stats-container, .tab-active, #toast, .modal-backdrop, #login-overlay, .filter-section {
                display: none !important;
            }
            .print-only { display: block !important; }
        }
        .print-only { display: none; }

        .custom-scroll::-webkit-scrollbar { width: 4px; }
        .custom-scroll::-webkit-scrollbar-track { background: #f1f1f1; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #868686; border-radius: 10px; }

        /* Ajustes Mobile para o Modal */
        @media (max-width: 768px) {
            .modal-container {
                max-height: 95vh;
                width: 95vw;
                overflow-y: auto !important;
                display: block !important; /* Muda de flex para block para permitir scroll natural */
            }
            .modal-side {
                width: 100% !important;
                height: auto !important;
                border-right: none !important;
            }
        }
    </style>
</head>
<body class="min-h-screen pb-12">

    <!-- Login Overlay -->
    <div id="login-overlay" class="fixed inset-0 bg-slate-50 z-[2000] flex items-center justify-center">
        <div class="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-sm text-center border border-slate-100">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpw58xdkWBtzFfHyOX7ky3OM_5OSEO401fHg&s" alt="Logo" class="w-24 mx-auto mb-6 rounded-xl">
            <h2 class="text-2xl font-bold text-slate-800 mb-2">Acesso ao Estoque</h2>
            <p class="text-sm text-slate-500 mb-8 italic">Chris Wellness Resort</p>
            <input type="password" id="access-pass" placeholder="Código de Acesso" class="w-full px-4 py-3 border border-slate-200 rounded-2xl outline-none text-center tracking-widest mb-4">
            <button onclick="window.checkAccess()" class="w-full btn-primary text-white font-bold py-4 rounded-2xl shadow-lg">Entrar</button>
            <p id="access-error" class="hidden text-red-500 text-xs mt-4">Código incorreto.</p>
        </div>
    </div>

    <!-- Loading Screen -->
    <div id="loading-screen" class="loading-overlay" style="display: none;">
        <div class="text-center">
            <div class="inline-block animate-spin rounded-full h-10 w-10 border-4 border-slate-300 border-t-slate-800 mb-2"></div>
            <p class="text-slate-500 text-sm">A carregar...</p>
        </div>
    </div>

    <div id="main-content" class="max-w-6xl mx-auto px-4 py-8 hidden">
        <header class="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-6 no-print">
            <div class="flex items-center gap-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpw58xdkWBtzFfHyOX7ky3OM_5OSEO401fHg&s" alt="Logo" class="w-12 h-12 rounded-lg object-cover">
                <div>
                    <h1 class="text-xl font-black text-slate-800">Chris Wellness <span class="font-light text-slate-500">Resort</span></h1>
                    <p class="text-slate-400 text-xs uppercase tracking-widest">Painel de Gestão</p>
                </div>
            </div>
            <div class="flex gap-3">
                <button onclick="window.openNewTransaction()" class="btn-primary text-white px-6 py-3 rounded-xl font-bold text-sm shadow-md">
                    <i class="fas fa-plus-circle mr-2"></i> Novo Registro
                </button>
            </div>
        </header>

        <!-- Stats -->
        <div id="stats-container" class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8 no-print"></div>

        <!-- Tabs -->
        <div class="flex gap-8 mb-6 border-b border-slate-200 px-2 no-print">
            <button onclick="window.switchTab('history')" id="tab-history" class="pb-3 font-bold text-sm text-slate-400 tab-active uppercase tracking-wider">Movimentações</button>
            <button onclick="window.switchTab('report')" id="tab-report" class="pb-3 font-bold text-sm text-slate-400 uppercase tracking-wider">Relatório Geral</button>
        </div>

        <!-- History View -->
        <div id="view-history" class="glass-card rounded-2xl overflow-hidden">
            <div class="p-6 border-b border-slate-50 flex flex-col sm:flex-row justify-between items-center gap-4 no-print">
                <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest">Últimos Lançamentos</h2>
                <input type="text" id="search-input" oninput="window.renderData()" placeholder="Procurar item..." class="px-4 py-2 bg-slate-50 border border-slate-100 rounded-xl text-sm outline-none w-full sm:w-64">
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left">
                    <thead class="bg-slate-50 text-[10px] text-slate-400 uppercase font-black">
                        <tr>
                            <th class="px-6 py-4">Data</th>
                            <th class="px-6 py-4">Item</th>
                            <th class="px-6 py-4">Setor</th>
                            <th class="px-6 py-4">Responsável</th>
                            <th class="px-6 py-4">Tipo</th>
                            <th class="px-6 py-4">Qtd</th>
                            <th class="px-6 py-4 text-right no-print">Ações</th>
                        </tr>
                    </thead>
                    <tbody id="inventory-body" class="divide-y divide-slate-50 text-slate-600 text-sm"></tbody>
                </table>
            </div>
        </div>

        <!-- Report View -->
        <div id="view-report" class="hidden glass-card rounded-2xl overflow-hidden">
            <div class="p-6 border-b border-slate-50 bg-slate-50/30 no-print">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                    <div>
                        <label class="text-[9px] font-black text-slate-400 uppercase mb-1 block">Filtrar Setor</label>
                        <select id="filter-category-report" onchange="window.renderData()" class="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs bg-white"></select>
                    </div>
                    <div>
                        <label class="text-[9px] font-black text-slate-400 uppercase mb-1 block">De</label>
                        <input type="date" id="report-date-start" onchange="window.renderData()" class="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs bg-white">
                    </div>
                    <div>
                        <label class="text-[9px] font-black text-slate-400 uppercase mb-1 block">Até</label>
                        <input type="date" id="report-date-end" onchange="window.renderData()" class="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs bg-white">
                    </div>
                    <button onclick="window.printReport()" class="bg-slate-800 text-white px-4 py-2.5 rounded-xl text-xs font-bold"><i class="fas fa-print mr-2"></i> Imprimir</button>
                </div>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left">
                    <thead class="bg-slate-50 text-[10px] text-slate-400 uppercase font-black">
                        <tr>
                            <th class="px-6 py-4">Produto</th>
                            <th class="px-6 py-4">Setor</th>
                            <th class="px-6 py-4">Entradas</th>
                            <th class="px-6 py-4">Saídas</th>
                            <th class="px-6 py-4">Saldo</th>
                            <th class="px-6 py-4">Status</th>
                        </tr>
                    </thead>
                    <tbody id="report-body" class="divide-y divide-slate-50 text-slate-600 text-sm"></tbody>
                </table>
            </div>
        </div>

        <div id="empty-state" class="hidden p-20 text-center">
            <p class="text-slate-400 italic">Nenhum dado encontrado para os filtros selecionados.</p>
        </div>
    </div>

    <!-- Modal Transaction -->
    <div id="modal-transacao" class="hidden fixed inset-0 z-[1500] flex items-center justify-center p-2 sm:p-4 bg-black/60 backdrop-blur-sm no-print">
        <div class="bg-white rounded-3xl w-full max-w-4xl shadow-2xl flex flex-col md:flex-row overflow-hidden modal-container">
            
            <!-- Left Side: Form Section -->
            <div class="w-full md:w-1/2 p-5 sm:p-6 border-b md:border-b-0 md:border-r border-slate-100 modal-side">
                <h3 class="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
                    <i class="fas fa-edit text-slate-400"></i> Registo de Fluxo
                </h3>
                <form id="item-form" class="space-y-4">
                    <div>
                        <label class="block text-[10px] font-black text-slate-400 uppercase mb-1">Produto</label>
                        <input type="text" id="prod-name" required list="products-list" autocomplete="off" 
                            oninput="window.handleProductInput()" placeholder="Ex: Toalha de Rosto"
                            class="w-full px-4 py-3 border border-slate-100 bg-slate-50 rounded-xl outline-none text-sm focus:ring-2 focus:ring-slate-200">
                        <datalist id="products-list"></datalist>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-[10px] font-black text-slate-400 uppercase mb-1">Setor</label>
                            <select id="prod-category-select" onchange="window.handleCategoryChange()" class="w-full px-4 py-3 border border-slate-100 bg-slate-50 rounded-xl outline-none text-sm">
                                <!-- Options dynamically injected -->
                            </select>
                            <input type="text" id="new-category-input" placeholder="Novo setor..." class="hidden mt-2 w-full px-4 py-2 border-2 border-slate-200 bg-slate-50 rounded-xl outline-none text-sm">
                        </div>
                        <div>
                            <label class="block text-[10px] font-black text-slate-400 uppercase mb-1">Quantidade</label>
                            <input type="number" id="prod-qty" required min="1" placeholder="0" class="w-full px-4 py-3 border border-slate-100 bg-slate-50 rounded-xl outline-none text-sm">
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-[10px] font-black text-slate-400 uppercase mb-1">Operação</label>
                            <select id="prod-type" class="w-full px-4 py-3 border border-slate-100 bg-slate-50 rounded-xl outline-none text-sm">
                                <option value="entrada">Entrada (+)</option>
                                <option value="saida">Saída (-)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-[10px] font-black text-slate-400 uppercase mb-1">Data</label>
                            <input type="date" id="prod-date" required class="w-full px-4 py-3 border border-slate-100 bg-slate-50 rounded-xl outline-none text-sm">
                        </div>
                    </div>

                    <div>
                        <label class="block text-[10px] font-black text-slate-400 uppercase mb-1">Responsável</label>
                        <input type="text" id="prod-responsible" required placeholder="Nome do colaborador" class="w-full px-4 py-3 border border-slate-100 bg-slate-50 rounded-xl outline-none text-sm">
                    </div>

                    <button type="button" onclick="window.addItemToBatch()" class="w-full border-2 border-dashed border-slate-300 text-slate-500 font-bold py-4 rounded-xl hover:bg-slate-50 transition-all text-sm mb-4 sm:mb-0">
                        <i class="fas fa-plus mr-2"></i> Adicionar à Lista
                    </button>
                </form>
            </div>

            <!-- Right Side: Batch Section -->
            <div class="w-full md:w-1/2 bg-slate-50/50 p-5 sm:p-6 flex flex-col modal-side">
                <h3 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Itens Aguardando Envio</h3>
                <div id="batch-list-container" class="flex-grow overflow-y-auto custom-scroll mb-4 space-y-2 pr-1 max-h-[250px] md:max-h-none min-h-[80px]">
                    <div class="flex items-center justify-center h-full text-slate-300 text-xs italic">Nenhum item adicionado</div>
                </div>
                
                <div class="pt-4 border-t border-slate-200 mt-auto bg-slate-50/50">
                    <button id="btn-submit-batch" disabled onclick="window.submitBatch()" class="w-full btn-primary text-white font-bold py-4 rounded-2xl shadow-xl disabled:opacity-50">
                        Confirmar e Gravar
                    </button>
                    <button onclick="window.toggleModal('modal-transacao')" class="w-full text-slate-400 text-[10px] font-black uppercase mt-3 hover:text-slate-600 p-3 block text-center">
                        <i class="fas fa-times mr-1"></i> Cancelar e Fechar
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Admin Password Modal -->
    <div id="modal-password" class="hidden fixed inset-0 z-[2500] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm no-print">
        <div class="bg-white rounded-3xl w-full max-w-sm p-8 text-center shadow-2xl">
            <i class="fas fa-lock text-slate-300 text-3xl mb-4"></i>
            <h3 class="text-xl font-bold text-slate-800 mb-6">Confirmar Código Admin</h3>
            <input type="password" id="admin-password" placeholder="••••" class="w-full px-4 py-4 border border-slate-100 bg-slate-50 rounded-2xl outline-none text-center text-2xl tracking-widest mb-4">
            <div id="password-error" class="hidden text-xs text-red-500 mb-4 font-bold italic">Código incorreto</div>
            <div class="flex gap-3">
                <button onclick="window.toggleModal('modal-password')" class="flex-1 px-4 py-3 text-slate-400 font-bold hover:bg-slate-50 rounded-xl">Cancelar</button>
                <button onclick="window.verifyPassword()" class="flex-1 px-4 py-3 bg-slate-800 text-white font-bold rounded-xl shadow-md">Confirmar</button>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-10 left-1/2 -translate-x-1/2 transform translate-y-20 opacity-0 transition-all duration-300 bg-slate-900 text-white px-8 py-4 rounded-2xl shadow-2xl z-[3000] no-print text-sm font-bold flex items-center gap-3 w-[90%] max-w-xs text-center justify-center">
        <i id="toast-icon" class="fas fa-check-circle text-emerald-400"></i>
        <span id="toast-text"></span>
    </div>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, collection, addDoc, onSnapshot, doc, deleteDoc, setDoc, query, getDocs } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        const firebaseConfig = JSON.parse(__firebase_config);
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const db = getFirestore(app);
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'hotel-chris-estoque';
        const ACCESS_PASS = "Hotel303021"; 

        let inventory = [];
        let categories = ["Copa/Restaurante", "Governança", "Manutenção", "SPA/Wellness", "Escritório", "Lazer"];
        let currentTab = 'history';
        let itemBatch = [];
        let pendingDeleteId = null;

        // --- AUTH & ACCESS ---
        window.checkAccess = () => {
            if (document.getElementById('access-pass').value === ACCESS_PASS) {
                document.getElementById('login-overlay').style.display = 'none';
                document.getElementById('main-content').classList.remove('hidden');
                document.getElementById('loading-screen').style.display = 'flex';
                initFirebase();
            } else {
                document.getElementById('access-error').classList.remove('hidden');
            }
        };

        const initFirebase = async () => {
            try {
                if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) await signInWithCustomToken(auth, __initial_auth_token);
                else await signInAnonymously(auth);
                onAuthStateChanged(auth, (user) => { if (user) startSync(); });
            } catch (e) {
                console.error("Auth error:", e);
                hideLoading();
            }
        };

        const startSync = () => {
            onSnapshot(collection(db, 'artifacts', appId, 'public', 'data', 'inventory'), (snap) => {
                inventory = snap.docs.map(d => ({ id: d.id, ...d.data() }));
                updateStats();
                updateProductsDatalist();
                window.renderData();
                hideLoading();
            }, (err) => console.error("Erro no inventário:", err));

            onSnapshot(doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'categories'), (snap) => {
                if (snap.exists()) {
                    categories = snap.data().list;
                    updateCategoryDropdowns();
                } else {
                    setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'categories'), { list: categories });
                }
            }, (err) => console.error("Erro nas categorias:", err));
        };

        const hideLoading = () => {
            const screen = document.getElementById('loading-screen');
            if (screen) { screen.style.opacity = '0'; setTimeout(() => screen.style.display = 'none', 500); }
        };

        window.toggleModal = (id) => {
            const modal = document.getElementById(id);
            if (modal) {
                modal.classList.toggle('hidden');
                // Bloquear scroll do body apenas em Desktop, em Mobile o modal container rola
                if (window.innerWidth > 768) {
                    document.body.style.overflow = modal.classList.contains('hidden') ? 'auto' : 'hidden';
                }
            }
        };

        window.switchTab = (tab) => {
            currentTab = tab;
            document.getElementById('view-history').classList.toggle('hidden', tab !== 'history');
            document.getElementById('view-report').classList.toggle('hidden', tab !== 'report');
            document.getElementById('tab-history').classList.toggle('tab-active', tab === 'history');
            document.getElementById('tab-report').classList.toggle('tab-active', tab === 'report');
            window.renderData();
        };

        const updateCategoryDropdowns = () => {
            const prodSelect = document.getElementById('prod-category-select');
            const reportSelect = document.getElementById('filter-category-report');
            const options = categories.map(c => `<option value="${c}">${c}</option>`).join('');
            if (prodSelect) prodSelect.innerHTML = options + `<option value="ADD_NEW">+ Nova Categoria</option>`;
            if (reportSelect) reportSelect.innerHTML = `<option value="ALL">Todos os Setores</option>` + options;
        };

        const updateProductsDatalist = () => {
            const list = document.getElementById('products-list');
            const uniqueNames = [...new Set(inventory.map(i => i.name))].sort();
            list.innerHTML = uniqueNames.map(n => `<option value="${n}">`).join('');
        };

        window.handleProductInput = () => {
            const name = document.getElementById('prod-name').value;
            const match = inventory.find(i => i.name.toLowerCase() === name.toLowerCase());
            if (match) {
                const select = document.getElementById('prod-category-select');
                const input = document.getElementById('new-category-input');
                select.value = match.category;
                input.classList.add('hidden');
                select.disabled = true;
            } else {
                document.getElementById('prod-category-select').disabled = false;
            }
        };

        window.handleCategoryChange = () => {
            const select = document.getElementById('prod-category-select');
            const input = document.getElementById('new-category-input');
            if (select.value === 'ADD_NEW') {
                input.classList.remove('hidden');
                input.focus();
            } else {
                input.classList.add('hidden');
                input.value = "";
            }
        };

        const getCurrentStock = (name) => {
            let stock = 0;
            inventory.forEach(i => {
                if (i.name.toLowerCase() === name.toLowerCase()) {
                    stock += (i.type === 'entrada' ? Number(i.qty) : -Number(i.qty));
                }
            });
            itemBatch.forEach(i => {
                if (i.name.toLowerCase() === name.toLowerCase()) {
                    stock += (i.type === 'entrada' ? Number(i.qty) : -Number(i.qty));
                }
            });
            return stock;
        };

        window.addItemToBatch = () => {
            const name = document.getElementById('prod-name').value.trim();
            const qty = Number(document.getElementById('prod-qty').value);
            const type = document.getElementById('prod-type').value;
            const date = document.getElementById('prod-date').value;
            const responsible = document.getElementById('prod-responsible').value.trim();
            let category = document.getElementById('prod-category-select').value;

            if (category === 'ADD_NEW') {
                category = document.getElementById('new-category-input').value.trim();
                if (!category) { showToast("Introduza o nome do novo setor.", "error"); return; }
            }

            if (!name || !qty || !date || !responsible || !category) {
                showToast("Preencha todos os campos.", "error");
                return;
            }

            if (type === 'saida') {
                const isRegistered = inventory.some(i => i.name.toLowerCase() === name.toLowerCase());
                if (!isRegistered) {
                    showToast(`O item "${name}" não existe no estoque.`, "error");
                    return;
                }
                const currentBalance = getCurrentStock(name);
                if (qty > currentBalance) {
                    showToast(`Estoque insuficiente: ${currentBalance} disponível.`, "error");
                    return;
                }
            }

            itemBatch.push({ name, qty, type, date, responsible, category, tempId: Date.now() });
            document.getElementById('prod-name').value = "";
            document.getElementById('prod-qty').value = "";
            document.getElementById('prod-name').focus();
            document.getElementById('prod-category-select').disabled = false;
            updateBatchUI();
        };

        const updateBatchUI = () => {
            const container = document.getElementById('batch-list-container');
            const submitBtn = document.getElementById('btn-submit-batch');
            submitBtn.disabled = itemBatch.length === 0;

            if (itemBatch.length === 0) {
                container.innerHTML = `<div class="flex items-center justify-center h-full text-slate-300 text-xs italic">Nenhum item adicionado</div>`;
                return;
            }

            container.innerHTML = itemBatch.map(item => `
                <div class="bg-white p-3 rounded-xl border border-slate-100 shadow-sm flex justify-between items-center group">
                    <div class="min-w-0">
                        <p class="text-sm font-bold text-slate-800 truncate">${item.name}</p>
                        <div class="flex gap-2 items-center">
                            <span class="text-[9px] px-1.5 py-0.5 rounded font-black uppercase ${item.type === 'entrada' ? 'bg-emerald-50 text-emerald-600' : 'bg-orange-50 text-orange-600'}">
                                ${item.type === 'entrada' ? '+' : '-'}${item.qty}
                            </span>
                            <span class="text-[9px] text-slate-400 font-medium">${item.category}</span>
                        </div>
                    </div>
                    <button onclick="window.removeItemFromBatch(${item.tempId})" class="text-slate-300 hover:text-red-400 p-2"><i class="fas fa-trash-alt"></i></button>
                </div>
            `).join('');
        };

        window.removeItemFromBatch = (id) => {
            itemBatch = itemBatch.filter(i => i.tempId !== id);
            updateBatchUI();
        };

        window.submitBatch = async () => {
            if (itemBatch.length === 0) return;
            const btn = document.getElementById('btn-submit-batch');
            btn.disabled = true;
            btn.innerHTML = `<i class="fas fa-spinner animate-spin mr-2"></i> Gravando...`;

            try {
                let updatedCats = [...categories];
                let hasNewCat = false;
                for (const item of itemBatch) {
                    if (!updatedCats.includes(item.category)) {
                        updatedCats.push(item.category);
                        hasNewCat = true;
                    }
                    const { tempId, ...cleanItem } = item;
                    await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'inventory'), cleanItem);
                }
                if (hasNewCat) await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'categories'), { list: updatedCats });
                showToast("Lançamentos guardados!");
                itemBatch = [];
                updateBatchUI();
                window.toggleModal('modal-transacao');
            } catch (e) {
                showToast("Erro ao guardar.", "error");
            } finally {
                btn.disabled = false;
                btn.innerText = "Confirmar e Gravar";
            }
        };

        window.renderData = () => {
            const emptyState = document.getElementById('empty-state');
            if (currentTab === 'history') {
                const search = document.getElementById('search-input').value.toLowerCase();
                const filtered = inventory.filter(i => i.name.toLowerCase().includes(search)).sort((a, b) => new Date(b.date) - new Date(a.date));
                emptyState.classList.toggle('hidden', filtered.length > 0);
                document.getElementById('inventory-body').innerHTML = filtered.map(item => `
                    <tr class="hover:bg-slate-50">
                        <td class="px-6 py-4 text-[10px] font-bold text-slate-400 whitespace-nowrap">${new Date(item.date).toLocaleDateString('pt-PT')}</td>
                        <td class="px-6 py-4 font-bold text-slate-800">${item.name}</td>
                        <td class="px-6 py-4"><span class="bg-slate-100 px-2 py-0.5 rounded text-[9px] font-bold uppercase">${item.category}</span></td>
                        <td class="px-6 py-4 text-xs font-medium">${item.responsible}</td>
                        <td class="px-6 py-4">
                            <span class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase ${item.type === 'entrada' ? 'bg-emerald-50 text-emerald-600' : 'bg-orange-50 text-orange-600'}">
                                ${item.type}
                            </span>
                        </td>
                        <td class="px-6 py-4 font-black text-slate-700">${item.qty}</td>
                        <td class="px-6 py-4 text-right no-print">
                            <button onclick="window.requestDelete('${item.id}')" class="text-slate-200 hover:text-red-400 p-2"><i class="fas fa-trash-alt text-xs"></i></button>
                        </td>
                    </tr>`).join('');
            } else {
                const catF = document.getElementById('filter-category-report').value;
                const dStart = document.getElementById('report-date-start').value;
                const dEnd = document.getElementById('report-date-end').value;
                const map = {};
                inventory.forEach(item => {
                    if (catF !== 'ALL' && item.category !== catF) return;
                    if (dStart && item.date < dStart) return;
                    if (dEnd && item.date > dEnd) return;
                    if (!map[item.name]) map[item.name] = { cat: item.category, in: 0, out: 0 };
                    item.type === 'entrada' ? map[item.name].in += Number(item.qty) : map[item.name].out += Number(item.qty);
                });
                const ks = Object.keys(map).sort();
                emptyState.classList.toggle('hidden', ks.length > 0);
                document.getElementById('report-body').innerHTML = ks.map(n => {
                    const balance = map[n].in - map[n].out;
                    return `
                    <tr class="hover:bg-slate-50">
                        <td class="px-6 py-4 font-bold text-slate-800">${n}</td>
                        <td class="px-6 py-4 text-[10px] font-bold text-slate-400">${map[n].cat}</td>
                        <td class="px-6 py-4 text-emerald-500 font-bold">+${map[n].in}</td>
                        <td class="px-6 py-4 text-orange-400 font-bold">-${map[n].out}</td>
                        <td class="px-6 py-4 font-black text-slate-700">${balance}</td>
                        <td class="px-6 py-4">
                            <span class="w-2.5 h-2.5 rounded-full inline-block ${balance < 5 ? 'bg-red-500 animate-pulse' : (balance < 15 ? 'bg-orange-400' : 'bg-emerald-400')}"></span>
                        </td>
                    </tr>`}).join('');
            }
        };

        const updateStats = () => {
            let inQ = 0, outQ = 0;
            inventory.forEach(i => i.type === 'entrada' ? inQ += Number(i.qty) : outQ += Number(i.qty));
            const container = document.getElementById('stats-container');
            if (container) {
                container.innerHTML = `
                    <div class="glass-card p-6 rounded-2xl">
                        <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Itens Únicos</p>
                        <h3 class="text-3xl font-black text-slate-800">${new Set(inventory.map(i => i.name)).size}</h3>
                    </div>
                    <div class="glass-card p-6 rounded-2xl">
                        <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Categorias</p>
                        <h3 class="text-3xl font-black text-slate-400">${categories.length}</h3>
                    </div>
                    <div class="glass-card p-6 rounded-2xl border-l-4 border-slate-800">
                        <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Saldo de Volume</p>
                        <h3 class="text-3xl font-black text-slate-700">${inQ - outQ}</h3>
                    </div>
                `;
            }
        };

        window.requestDelete = (id) => { pendingDeleteId = id; window.toggleModal('modal-password'); };
        window.verifyPassword = async () => {
            const val = document.getElementById('admin-password').value;
            if (val === ACCESS_PASS) {
                await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'inventory', pendingDeleteId));
                showToast("Registo removido.");
                window.toggleModal('modal-password');
                document.getElementById('admin-password').value = "";
            } else {
                document.getElementById('password-error').classList.remove('hidden');
            }
        };

        window.openNewTransaction = () => {
            document.getElementById('item-form').reset();
            document.getElementById('prod-date').value = new Date().toISOString().split('T')[0];
            document.getElementById('new-category-input').classList.add('hidden');
            document.getElementById('prod-category-select').disabled = false;
            itemBatch = [];
            updateBatchUI();
            window.toggleModal('modal-transacao');
        };

        const showToast = (msg, type = "success") => {
            const t = document.getElementById('toast');
            const icon = document.getElementById('toast-icon');
            document.getElementById('toast-text').innerText = msg;
            icon.className = type === 'success' ? 'fas fa-check-circle text-emerald-400' : 'fas fa-exclamation-triangle text-orange-400';
            t.classList.replace('translate-y-20', 'translate-y-0');
            t.classList.replace('opacity-0', 'opacity-100');
            setTimeout(() => {
                t.classList.replace('translate-y-0', 'translate-y-20');
                t.classList.replace('opacity-100', 'opacity-0');
            }, 3000);
        };

        window.printReport = () => window.print();

    </script>
</body>
</html>
