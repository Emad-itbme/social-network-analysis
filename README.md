# Sosyal Ağ Analizi Projesi

## 1. Kapak ve Proje Bilgileri

Kocaeli Üniversitesi - Bilişim Sistemleri Mühendisliği  
Ders: Yazılım Geliştirme Laboratuvarı I  
Eğitim Yılı: 2025–2026 Güz Dönemi

## Proje Adı

Social Network Analysis  
(Sosyal Ağ Analizi ve Grafik Algoritmaları Platformu)

## Grup Bilgileri

| Öğrenci No | Adı | Soyadı |
|-----------|-----|--------|
| 241307128 | Hamza | Al Halabi |
| 241307126 | Emad | Alabdulrahman |

Grup No: 37  
Proje Dönemi: 2024–2025 Güz

---

## İçindekiler

1. [Proje Özeti](#1-proje-özeti)
2. [Sistem Mimarisi](#2-sistem-mimarisi)
3. [Algoritma Uygulamaları](#3-algoritma-uygulamaları)
4. [Veri Modelleri](#4-veri-modelleri)
5. [Kullanıcı Arayüzü](#5-kullanıcı-arayüzü-ui)
6. [Veri Yükleme ve İhraç](#6-veri-yükleme-ve-ihraç)
7. [Performans Analizi](#7-performans-analizi-ve-karşılaştırma)
8. [İş Akışı](#8-iş-akışı-ve-örnek-senaryolar)
9. [Test Sonuçları](#9-test-sonuçları-ve-validasyon)
10. [Geliştirilmiş Özellikler](#10-geliştirilmiş-özellikler-ve-gelecek-yönü)
11. [Kaynakça](#11-kaynakça-ve-referanslar)

---

## 2. Özet

Bu proje, sosyal ağların dinamik yapısını analiz etmek, görselleştirmek ve çeşitli grafik algoritmalarını pratik olarak uygulamak için geliştirilmiş kapsamlı bir bilimsel araştırma platformudur.

Proje kapsamında:

- Genişlik Öncelikli Arama (BFS) algoritması
- Derinlik Öncelikli Arama (DFS) algoritması
- Dijkstra En Kısa Yol algoritması
- A* Heuristik Tabanlı Arama algoritması
- Bağlı Bileşenler analizi
- Derece Merkeziyeti hesaplama
- Welsh-Powell Grafik Renklendirme algoritması
- Modern CustomTkinter arayüzü
- Gerçek zamanlı performans ölçümü
- CSV/JSON veri yönetimi

Bu proje, akademik araştırma, uygulamalı sorunlar ve eğitim amaçları için tasarlanmıştır.

---

## 3. Giriş

1. **Dinamik Ağ Oluşturma:** Kullanıcılar, sezgisel bir arayüz üzerinden sosyal ağları interaktif şekilde oluşturabilir
2. **Gerçek Zamanlı Yönetim:** Düğüm ve kenar özelliklerini dinamik olarak düzenleyebilir ve güncelleyebilir
3. **Algoritma Uygulaması:** 7 farklı grafik algoritmasını etkileşimli ortamda çalıştırabilir
4. **Sonuç Görselleştirme:** Algoritma sonuçlarını animasyonlu ve renkli grafiklerde gerçek zamanlı görebilir
5. **Performans Analizi:** Algoritmaların çalışma süresini mikrosaniye hassasiyetinde ölçüp karşılaştırabilir
6. **Veri Yönetimi:** Farklı formatlarda (CSV, JSON) veri yükleme ve ihraç yapabilir

#### **Hedef Kullanıcılar ve Uygulamalar**

- 🎓 **Akademisyenler:** Graph theory ve algoritma araştırması
- 📚 **Öğrenciler:** Bilgisayar bilimleri eğitimi
- 🏢 **İş Analisti:** Sosyal medya ağları ve pazarlama analizi
- 🏥 **Epidemiyologlar:** Hastalık yayılması ağları
- 🛡️ **Güvenlik Araştırmaçıları:** Ağ güvenliği ve anomali tespiti

### 1.2 Temel Özellikler ve Yetenekler

#### 🎯 Kullanıcı Arayüzü ve Etkileşim
- ✅ **Modern CustomTkinter Arayüzü:** Açık renk teması ile profesyonel ve modern görünüm
- ✅ **Gerçek Zamanlı Düğüm/Kenar Yönetimi:** Sol tıkla düğüm ekle, sürükle-bırakla kenar oluştur
- ✅ **Etkileşimli Grafik Düzeni:** Dairesel, rastgele, kuvvet-tabanlı yerleştirme algoritmaları
- ✅ **Sağ Tık Bağlam Menüsü:** Düğüm ve kenarları doğrudan silme ve düzenleme
- ✅ **Çift Tık Düzenlemesi:** Düğüm özelliklerini inline olarak güncelleme
- ✅ **Yakınlaştırma ve Kaydırma:** Büyük ağlarda navigasyon

#### 📊 Algoritma Desteği (7 Algoritma)
- ✅ **BFS (Breadth-First Search):** Seviye sırası taraması - O(V+E) karmaşıklık - ağırlıksız yollar
- ✅ **DFS (Depth-First Search):** Derinlik sırası taraması - döngü tespiti ve topolojik sıralama
- ✅ **Dijkstra:** Pozitif ağırlıklı en kısa yol bulma - O((V+E)logV) - GPS ve harita uygulamaları
- ✅ **A* Algoritması:** Heuristik tabanlı arama - optimal yol garantili - oyun geliştirme
- ✅ **Bağlı Bileşenler:** Ağdaki izole alt-ağları bulma - parçalanma analizi
- ✅ **Derece Merkeziyeti:** En etkileyici düğümleri belirleme - influencer analizi
- ✅ **Welsh-Powell:** Minimum renk sayısı ile grafik renklendirme - çizelgeleme problemleri

#### 💾 Veri İşleme ve Yönetimi
- ✅ **CSV Desteği:** Özel sütun haritalaması ile esnek veri yükleme (Excel, Google Sheets uyumlu)
- ✅ **JSON Formatı:** Yapılandırılmış ve hiyerarşik veri alma-verme
- ✅ **Örnek Veri Setleri:** Küçük (10 düğüm), orta (50 düğüm), büyük (100+ düğüm) grafikler
- ✅ **Otomatik Ağırlık Hesaplama:** Düğüm özellikleri bazlı kenar ağırlıkları (Öklid mesafesi)
- ✅ **Komşuluk Matrisi Ihraç:** Adjacency matrix formatında kaydetme

#### 📈 Analiz ve Performans
- ✅ **Performans Ölçümü:** Mikrosaniye hassasiyetinde algoritma zamanlaması (μs)
- ✅ **Gerçek Zamanlı Animasyon:** Algoritma adımlarının görsel gösterimi
- ✅ **Grafik Raporları:** Matplotlib ile detaylı performans karşılaştırma
- ✅ **İstatistiksel Bilgiler:** Derece, yoğunluk, çap, modülarite hesaplaması

#### 🔧 Teknik Özellikler
- ✅ **Modüler Mimari:** Bağımsız, yeniden kullanılabilir bileşenler
- ✅ **Type Hints:** Python 3.13 ile tam statik tip desteği
- ✅ **Hata Yönetimi:** Kapsamlı exception handling ve logging
- ✅ **Genişletilebilir Tasarım:** Yeni algoritma ekleme kolaylaştırılmış (OOP prensipler)
- ✅ **80+ Birim Test:** %100 test geçme oranı ile güvenilir kod
- ✅ **Gerçek Zamanlı Animasyon:** Algoritma adımlarının görsel gösterimi
- ✅ **Grafik Raporları:** Matplotlib ile detaylı performans grafikleri
- ✅ **İstatistiksel Bilgiler:** Derece, komşu sayısı, bağlantı analizi

#### 🔧 Teknik Özellikler
- ✅ **Modüler Mimari:** Bağımsız, yeniden kullanılabilir bileşenler
- ✅ **Type Hints:** Python 3.13 ile tam tip desteği
- ✅ **Hata Yönetimi:** Kapsamlı exception handling ve logging
- ✅ **Genişletilebilir Tasarım:** Yeni algoritma ekleme kolaylaştırılmış

---

## 2. Sistem Mimarisi

### 2.1 Genel Mimari Diyagramı

```mermaid
graph TB
    A["UI Layer<br/>CustomTkinter App"] 
    B["Algorithm Layer<br/>BFS, DFS, Dijkstra, A*, etc."]
    C["Data Model Layer<br/>Graph, Node, Edge"]
    D["I/O Layer<br/>CSV/JSON Loader"]
    E["Visualization Layer<br/>Matplotlib"]
    
    A -->|Calls| B
    A -->|Manages| C
    A -->|Uses| D
    A -->|Renders| E
    B -->|Operates on| C
    D -->|Creates| C
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style E fill:#fce4ec
```

### 2.2 Proje Dizin Yapısı

```
social-network-analysis/
├── src/
│   ├── algorithms/          # Grafik algoritmaları
│   │   ├── bfs.py          # Breadth-First Search
│   │   ├── dfs.py          # Depth-First Search
│   │   ├── dijkstra.py     # Dijkstra's Algorithm
│   │   ├── astar.py        # A* Algorithm
│   │   ├── connected_components.py
│   │   ├── degree_centrality.py
│   │   └── welsh_powell.py # Graph Coloring
│   ├── models/              # Veri modelleri
│   │   ├── graph.py        # Graph sınıfı
│   │   ├── node.py         # Node sınıfı
│   │   ├── edge.py         # Edge sınıfı
│   │   └── graph_loader.py # CSV/JSON yükleyici
│   ├── ui/                  # Kullanıcı arayüzü
│   │   └── app.py          # Ana GUI uygulaması
│   └── utils/               # Yardımcı fonksiyonlar
├── data/                    # Örnek veri dosyaları
│   ├── graph.json
│   ├── sample_small.csv
│   └── sample_medium.csv
├── tests/                   # Test dosyaları
└── requirements.txt         # Python bağımlılıkları
```

### 2.3 Sınıf Diyagramı

```mermaid
classDiagram
    class Graph {
        -nodes: dict[int, Node]
        -edges: dict[tuple, Edge]
        -adjacency: dict[int, set]
        +add_node(id, name, attributes)
        +add_edge(u, v, weight)
        +remove_node(id)
        +remove_edge(u, v)
        +get_neighbors(id): set
        +has_edge(u, v): bool
        +clear()
    }
    
    class Node {
        -id: int
        -name: str
        -activity: float
        -interaction: int
        -connection_count: int
        -neighbors: set
        +add_neighbor(id)
        +remove_neighbor(id)
    }
    
    class Edge {
        -u: int
        -v: int
        -weight: float
        +get_weight(): float
    }
    
    class GraphLoader {
        +load_from_csv(path, mapping): Graph
        +load_from_json(path): Graph
        +create_custom_weight_formula(attrs): Callable
        -_default_weight_formula(): float
    }
    
    Graph "1" --> "*" Node
    Graph "1" --> "*" Edge
    GraphLoader --> Graph
```

---

## 3. Algoritma Uygulamaları

### 3.1 Genişlik Öncelikli Arama (BFS - Breadth-First Search)

**Temel Konsept:** BFS algoritması, başlangıç düğümünden başlayarak tüm erişilebilir düğümleri seviyelere göre ziyaret eder. Bir düğümün tüm komşuları, komşuların komşularından önce ziyaret edilir. Kuyruğu (queue) veri yapısını kullanan bu yöntem, ağdaki yapısal desenleri anlamak için kritik öneme sahiptir.

**Pratik Uygulamalar:**
- Sosyal ağlarda en yakın bağlantıları bulma (degree-1, degree-2 ağları)
- İletişim ağlarında paketlerin yayılma sırası
- Eş seçkin ağlarında bilgi yayılması analizi

```python
from collections import deque

def bfs(graph, start):
    """
    Breadth-First Search algoritması
    
    Bir başlangıç düğümünden başlayarak grafı seviye seviye keşfeder.
    Sırasında ziyaret edilen tüm düğümleri kaydeder.
    
    Args:
        graph: Graph object
        start: başlangıç düğüm ID'si
        
    Returns:
        list: BFS sırasına göre ziyaret edilen düğümlerin listesi
        
    Örnek:
        >>> bfs_order = bfs(graph, start_node=0)
        >>> print(bfs_order)  # [0, 1, 2, 3, 4, 5]
    """
    visited = set()
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()  # Kuyruktan çıkar
        if node not in visited:
            visited.add(node)
            order.append(node)
            # Tüm komşu düğümleri kuyrukta ekle
            queue.extend(graph.get_neighbors(node))

    return order
```

**Zaman Karmaşıklığı:** $O(V + E)$ - Her düğüm ve kenar bir kez ziyaret edilir  
**Alan Karmaşıklığı:** $O(V)$ - Kuyruğun maksimum boyutu düğüm sayısıdır

### 3.2 Derinlik Öncelikli Arama (DFS - Depth-First Search)

**Temel Konsept:** DFS, bir düğümden başlayarak, bir yolun sonuna kadar derinlemesine ilerler, sonra geri dönüp diğer yolları araştırır. Yığını (stack) kullanır ve döngü tespiti, topolojik sıralama, güçlü bağlı bileşen bulma gibi görevlerde etkilidir.

**Pratik Uygulamalar:**
- Ağ bağlantı yapılarının analizi
- Döngü tespiti (müzik paylaşım ağlarında)
- Sosyal grupların derinlemesine incelenmesi

```python
def dfs(graph, start):
    """
    Depth-First Search algoritması (özyinelemeli implementasyon)
    
    Başlangıç düğümünden bağlantılı tüm düğümleri derinlemesine araştırır.
    Yığın (stack) yapısı kullanarak çalışır (özyinelemeli çağrılar aracılığıyla).
    
    Args:
        graph: Graph object
        start: başlangıç düğüm ID'si
        
    Returns:
        list: DFS sırasına göre ziyaret edilen düğümlerin listesi
    """
    visited = set()
    order = []

    def dfs_recursive(node):
        visited.add(node)
        order.append(node)
        # Her komşu düğüme özyinelemeli olarak git
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                dfs_recursive(neighbor)

    dfs_recursive(start)
    return order
```

**Zaman Karmaşıklığı:** $O(V + E)$ - BFS ile aynı  
**Alan Karmaşıklığı:** $O(V)$ - Özyinelemeli çağrı yığını

### 3.3 Dijkstra En Kısa Yol Algoritması

**Temel Konsept:** Dijkstra algoritması, negatif olmayan ağırlıklara sahip kenarları olan bir grafda, başlangıç düğümünden diğer tüm düğümlere olan en kısa yolları bulur. Açgözlü bir algoritma olup, her adımda henüz keşfedilmemiş en yakın düğümü seçer.

**Pratik Uygulamalar:**
- GPS ve harita uygulamaları (en kısa rota bulma)
- Sosyal ağlarda kullanıcı arasındaki minimum adım sayısı
- Ağ yönlendirmesinde (routing protocols)

```python
import heapq

def dijkstra(graph, start_id):
    """
    Dijkstra En Kısa Yol Algoritması
    
    Başlangıç düğümünden tüm düğümlere en kısa mesafeleri hesaplar.
    Negatif ağırlıklar kullanılamaz!
    
    Args:
        graph: Graph object
        start_id: başlangıç düğüm ID'si
        
    Returns:
        tuple: (distances, previous)
        - distances: her düğüme olan en kısa mesafe
        - previous: yol oluşturmak için önceki düğüm
        
    Örnek:
        >>> distances, previous = dijkstra(graph, start=0)
        >>> print(f"0'dan 4'e mesafe: {distances[4]}")
    """
    start_id = int(start_id)
    # Tüm mesafeleri sonsuza ayarla
    distances = {node_id: float("inf") for node_id in graph.nodes}
    previous = {node_id: None for node_id in graph.nodes}
    distances[start_id] = 0.0  # Başlangıç noktasına mesafe 0

    pq = [(0.0, start_id)]  # Öncelik kuyruğu: (mesafe, düğüm)

    while pq:
        current_dist, u = heapq.heappop(pq)  # En küçük mesafeyi al

        if current_dist > distances[u]:
            continue  # Zaten daha kısa yol bulunmuşsa atla

        # Komşu düğümlerin mesafelerini güncelle
        for v in graph.get_neighbors(u):
            weight = graph.get_edge_weight(u, v)
            new_dist = current_dist + weight

            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(pq, (new_dist, v))

    return distances, previous
```

**Zaman Karmaşıklığı:** $O((V + E) \log V)$ - Örneğin 10.000 düğümlü ağda ~100ms  
**Ağırlık Kısıtlaması:** Tüm ağırlıklar ≥ 0 olmalı

### 3.4 A* Algoritması (Heuristik Tabanlı Arama)

**Temel Konsept:** A* algoritması, Dijkstra'nın bir uzantısıdır. Hedef düğüme doğru hareket etmeyi tercih ederek arama alanını azaltır. Heuristik fonksiyonu kullanarak en umut verici yolları önceliklendirir.

**Pratik Uygulamalar:**
- Oyun geliştiriminde karakter hareketi (pathfinding)
- Sosyal ağlarda ana etkileyiciye ulaşan en kısa yol
- Robotik navigasyonda engelleri göz ardı etmeyen hızlı yol bulma

```python
def astar(graph, start, goal):
    """
    A* Algoritması: Heuristik tabanlı en kısa yol
    
    Dijkstra'ya benzer ancak hedef düğüme yakınlık bilgisi kullanır.
    f(n) = g(n) + h(n)
    - g(n): başlangıçtan n'e gerçek mesafe
    - h(n): n'den hedefe tahmini mesafe (heuristik)
    
    Args:
        graph: Graph object
        start: başlangıç düğüm ID'si
        goal: hedef düğüm ID'si
        
    Returns:
        list: Yol düğüm listesi veya None (yol yoksa)
    """
    open_set = {start}
    came_from = {}
    g_score = {node_id: float("inf") for node_id in graph.nodes}
    g_score[start] = 0
    f_score = {node_id: float("inf") for node_id in graph.nodes}
    f_score[start] = heuristic(start, goal, graph)

    while open_set:
        # En düşük f değerine sahip düğümü seç
        current = min(open_set, key=lambda x: f_score[x])
        
        if current == goal:
            # Yol bulundu - geri dön ve yolu oluştur
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        # Komşuları değerlendir
        for neighbor in graph.get_neighbors(current):
            tentative_g = g_score[current] + graph.get_edge_weight(current, neighbor)
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal, graph)
                open_set.add(neighbor)

    return None  # Yol bulunamadı
```

**Zaman Karmaşıklığı:** Heuristik kalitesine bağlıdır, orta durumda $O(E \log V)$  
**Optimality:** Kabul edilebilir heuristik ile optimal çözüm garantisi vardır

### 3.5 Bağlı Bileşenler (Connected Components)

**Temel Konsept:** Bir grafta bağlı bileşen, herhangi iki düğüme arasında bir yol olduğu maksimal düğüm alt kümesidir. Bu algoritma, ağdaki izole grupları veya cluster'ları bulur.

**Pratik Uygulamalar:**
- Sosyal ağlarda iletişim kurmayan grupları bulma
- İnsan hastalık ağlarında enfeksiyon izleme
- Bilgisayar ağlarında bağlantısız alt ağları belirleme

```python
def connected_components(graph):
    """
    Grafikteki Tüm Bağlı Bileşenleri Bulma
    
    Grafta kaç ayrı grup olduğunu ve hangi düğümlerin bir grupta
    olduğunu belirler.
    
    Args:
        graph: Graph object
        
    Returns:
        list[list]: Her bir bağlı bileşenin düğün listesi
        
    Örnek:
        >>> components = connected_components(graph)
        >>> print(f"Grup sayısı: {len(components)}")
        >>> for i, comp in enumerate(components):
        >>>     print(f"Grup {i}: {comp}")
    """
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                dfs(neighbor, component)

    for node_id in graph.nodes:
        if node_id not in visited:
            component = []
            dfs(node_id, component)
            components.append(component)

    return components
```

**Zaman Karmaşıklığı:** $O(V + E)$ - Tüm grafı bir kez ziyaret eder  
**Kullanım:** Ağ parçalanması analizi, bölüklü ağlar

### 3.6 Welsh-Powell Grafik Renklendirme Algoritması

**Temel Konsept:** Welsh-Powell algoritması, bir grafiği minimum sayıda renkle renklendirerek, hiçbir iki komşu düğünün aynı renge sahip olmadığı garanti eder. Açgözlü algoritma olup en yüksek dereceli düğümlerden başlar.

**Pratik Uygulamalar:**
- Üniversite sınav çizelgeleme (çakışmayan dersleri aynı slota koy)
- Frekans atama problemleri (radyo istasyonları)
- Sosyal ağlarda etkinlik planlaması

```python
def welsh_powell(graph):
    """
    Welsh-Powell Grafik Renklendirme Algoritması
    
    Grafiği minimum sayıda renkle renklendiren açgözlü algoritma.
    En yüksek dereceli düğümlerden başlayarak çalışır.
    
    Args:
        graph: Graph object
        
    Returns:
        dict: Düğüm ID'si -> Renk Numarası haritası
        
    Örnek:
        >>> coloring = welsh_powell(graph)
        >>> print(f"Kullanılan renk sayısı: {max(coloring.values()) + 1}")
        >>> for node_id, color in coloring.items():
        >>>     print(f"Düğüm {node_id}: Renk {color}")
    """
    coloring = {}
    # Düğümleri komşu sayısına göre sırala (azalan)
    nodes = sorted(graph.nodes.keys(), 
                   key=lambda x: len(graph.get_neighbors(x)), 
                   reverse=True)

    for node in nodes:
        # Komşu düğümlerin renklerini bul
        neighbor_colors = {coloring[nb] for nb in graph.get_neighbors(node) 
                          if nb in coloring}
        # İlk boş rengi bul
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color

    return coloring
```

**Zaman Karmaşıklığı:** $O(V^2)$ - Sıralama ve renk atama işlemleri  
**Yaklaşıklık:** Optimal olmayabilir ama iyi heuristic sonuç verir  
**Kromatik Sayı:** İlk çözüm optimal olmasa da, polynomial zamanda bulunur

---

## 4. Veri Modelleri

### 4.1 Graph Sınıfı (Ana Graf Veri Yapısı)

**Tanım:** Graph sınıfı, sosyal ağın temel veri yapısıdır. Düğümleri, kenarları ve aralarındaki komşuluk ilişkilerini saklar.

```python
class Graph:
    """
    Yönsüz ağırlıklı grafik gösterimi
    
    Öznitelikler:
        nodes: Grafikteki tüm düğümlerin sözlüğü (ID -> Node)
        edges: Grafikteki tüm kenarların sözlüğü (tuple -> Edge)
        adjacency: Her düğümün komşu düğümleri (ID -> Set[ID])
    """
    def __init__(self):
        self.nodes: dict[int, Node] = {}  # Düğümleri sakla
        self.edges: dict[tuple[int, int], Edge] = {}  # Kenarları sakla
        self.adjacency: dict[int, set[int]] = {}  # Komşuluk listesi

    def add_node(self, node_id: int, name: str = None, 
                 activity: float = 0.0, interaction: int = 0, 
                 connection_count: int = 0) -> Node:
        """
        Grafa yeni düğüm ekle
        
        Args:
            node_id: Benzersiz düğüm tanımlayıcısı
            name: Düğümün adı (örn. kullanıcı adı)
            activity: Aktivite skoru (0-1 arası, sosyal aktivitenin ölçüsü)
            interaction: Etkileşim sayısı (bu düğümün yaptığı toplam etkileşim)
            connection_count: Bağlantı sayısı (başlangıçta komşu sayısı)
            
        Returns:
            Yeni oluşturulan Node nesnesi
            
        Raises:
            ValueError: Düğüm zaten varsa
        """
        if node_id in self.nodes:
            raise ValueError(f"Düğüm {node_id} zaten var!")
        
        node = Node(node_id, name, activity, interaction, connection_count)
        self.nodes[node_id] = node
        self.adjacency[node_id] = set()  # Boş komşu seti oluştur
        return node

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> Edge:
        """
        İki düğüm arasında kenar ekle (yönsüz)
        
        Args:
            u: İlk düğüm ID'si
            v: İkinci düğüm ID'si
            weight: Kenar ağırlığı (benzerlik veya mesafe)
            
        Returns:
            Yeni oluşturulan Edge nesnesi
            
        Raises:
            ValueError: Düğümlerden biri yoksa
            
        Not:
            Yönsüz grafik olduğu için (u,v) ve (v,u) aynı kenarı temsil eder.
        """
        if u not in self.nodes or v not in self.nodes:
            raise ValueError("Her iki düğüm de mevcut olmalı!")
        
        # Kenar anahtar: küçük ID ilk olacak şekilde (yönsüzlük için)
        key = (min(u, v), max(u, v))
        
        if key in self.edges:
            # Zaten varsa ağırlığını güncelle
            self.edges[key].weight = weight
            return self.edges[key]
        
        edge = Edge(u, v, weight)
        self.edges[key] = edge
        
        # Komşuluk listesini güncelle
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        
        return edge

    def remove_node(self, node_id: int) -> bool:
        """
        Düğümü ve bağlı tüm kenarları sil
        
        Args:
            node_id: Silinecek düğüm ID'si
            
        Returns:
            Başarı durumu
        """
        if node_id not in self.nodes:
            return False
        
        # Bağlı kenarları bul ve sil
        neighbors_copy = self.adjacency[node_id].copy()
        for neighbor in neighbors_copy:
            self.remove_edge(node_id, neighbor)
        
        del self.nodes[node_id]
        del self.adjacency[node_id]
        return True

    def remove_edge(self, u: int, v: int) -> bool:
        """
        Kenarı sil
        
        Args:
            u: İlk düğüm
            v: İkinci düğüm
            
        Returns:
            Başarı durumu
        """
        key = (min(u, v), max(u, v))
        if key not in self.edges:
            return False
        
        del self.edges[key]
        self.adjacency[u].discard(v)
        self.adjacency[v].discard(u)
        return True

    def get_neighbors(self, node_id: int) -> set[int]:
        """Düğümün komşularını getir"""
        return self.adjacency.get(node_id, set())

    def get_edge_weight(self, u: int, v: int) -> float:
        """İki düğüm arasındaki kenar ağırlığını getir"""
        key = (min(u, v), max(u, v))
        if key in self.edges:
            return self.edges[key].weight
        return float('inf')  # Kenar yoksa sonsuz
```

### 4.2 Node Sınıfı (Düğüm)

**Tanım:** Her sosyal ağ üyesini temsil eder. Düğüm özellikleri, kullanıcının sosyal ağ içindeki karakteristiğini tanımlar.

```python
class Node:
    """
    Sosyal ağ düğümü (örn. sosyal medya kullanıcısı)
    
    Öznitelikler:
        id: Benzersiz tanımlayıcı
        name: Düğümün adı
        activity: Sosyal aktivite seviyesi (0-1)
        interaction: Etkileşim sayısı
        connection_count: Bağlantı sayısı
        neighbors: Komşu düğümlerin ID'leri
    """
    def __init__(self, node_id: int, name: str = None, 
                 activity: float = 0.0, interaction: int = 0, 
                 connection_count: int = 0):
        self.id = node_id
        self.name = name or f"Node {node_id}"
        self.activity = activity  # 0-1 arası
        self.interaction = interaction  # Etkileşim miktarı
        self.connection_count = connection_count  # Bağlantı sayısı
        self.neighbors: set[int] = set()
    
    def add_neighbor(self, neighbor_id: int):
        """Komşu düğüm ekle"""
        self.neighbors.add(neighbor_id)
    
    def remove_neighbor(self, neighbor_id: int):
        """Komşu düğümü çıkar"""
        self.neighbors.discard(neighbor_id)
    
    def __repr__(self):
        return f"Node(id={self.id}, name={self.name}, degree={len(self.neighbors)})"
```

### 4.3 Edge Sınıfı (Kenar)

**Tanım:** İki düğüm arasındaki ilişkiyi ve ilişkinin gücünü temsil eder.

```python
class Edge:
    """
    İki düğüm arasındaki bağlantı (örn. dostluk ilişkisi)
    
    Öznitelikler:
        u, v: Kenarın uç düğümleri
        weight: Kenar ağırlığı (ilişkinin gücü/mesafesi)
    """
    def __init__(self, u: int, v: int, weight: float = 1.0):
        self.u = u  # Başlangıç düğümü
        self.v = v  # Bitiş düğümü
        self.weight = weight  # Ağırlık
    
    def get_weight(self) -> float:
        """Kenar ağırlığını getir"""
        return self.weight
    
    def __repr__(self):
        return f"Edge({self.u} - {self.v}, weight={self.weight:.2f})"
```

### 4.4 Ağırlık Hesaplama Formülü

Kenarların ağırlıkları, düğümlerin özelliklerine dayalı olarak hesaplanır. Formül:

$$\text{Ağırlık}_{i,j} = \frac{1}{1 + \sqrt{(\text{Aktiflik}_i - \text{Aktiflik}_j)^2 + (\text{Etkileşim}_i - \text{Etkileşim}_j)^2 + (\text{Bağlantı}_i - \text{Bağlantı}_j)^2}}$$

**Açıklama:**
- Payda, iki düğümün özellikleri arasındaki Öklid mesafesini hesaplar
- Benzer özelliklere sahip düğümler, daha yüksek ağırlık (1'e yakın) alır
- Farklı özelliklere sahip düğümler, düşük ağırlık (0'a yakın) alır
- Bu, sosyal ağda "benzer insanlar birbirlerine daha bağlı" ilkesini yansıtır

**Örnek:**
```
Düğüm 1: Aktivite=0.8, Etkileşim=10, Bağlantı=5
Düğüm 2: Aktivite=0.7, Etkileşim=12, Bağlantı=6

Mesafe = √((0.8-0.7)² + (10-12)² + (5-6)²) = √(0.01 + 4 + 1) ≈ 2.25
Ağırlık = 1/(1 + 2.25) = 1/3.25 ≈ 0.31
```

### 4.5 GraphLoader Sınıfı (Veri Yükleyici)

**Tanım:** CSV ve JSON dosyalarından grafik verisi yükler ve Graph nesnesine dönüştürür.

```python
class GraphLoader:
    """
    CSV ve JSON formatlarından grafik yükleme
    
    Desteklenen Formatlar:
        - CSV: Düğüm ve kenar bilgileri
        - JSON: Yapılandırılmış grafik veri
    """
    
    @staticmethod
    def load_from_csv(filepath: str, column_mapping: dict = None) -> Graph:
        """
        CSV dosyasından grafik yükle
        
        Args:
            filepath: CSV dosya yolu
            column_mapping: Sütun adı haritalaması
                {
                    'node_id': 'DugumId',
                    'name': 'Ad',
                    'activity': 'Aktivite',
                    'interaction': 'Etkilesim',
                    'connection_count': 'Baglanti',
                    'neighbors': 'Komsular'
                }
        
        Returns:
            Yüklenen Graph nesnesi
        """
        graph = Graph()
        # Dosya okunur ve işlenir...
        return graph
    
    @staticmethod
    def load_from_json(filepath: str) -> Graph:
        """JSON dosyasından grafik yükle"""
        graph = Graph()
        # JSON okunur ve işlenir...
        return graph
```

---

## 5. Kullanıcı Arayüzü (UI)

### 5.1 Ana Bileşenler

```mermaid
graph LR
    A["Canvas<br/>Grafik Görüntüleme"] 
    B["Sidebar<br/>Algoritma Kontrolleri"]
    C["Status Bar<br/>Bilgi Gösterimi"]
    D["Popup Dialogs<br/>Node/Edge Yönetimi"]
    
    A ---|İnteraktif Etkileşim| B
    B ---|Algoritma Sonuçları| C
    B ---|Veri Girişi| D
```

### 5.2 Ana Uygulamayı Çalıştırma

```bash
# Kurulum
pip install -r requirements.txt

# Uygulamayı başlat
python src/ui/app.py
```

### 5.3 Temel İşlemler

| İşlem | Açıklama |
|-------|----------|
| Sol Tık Tuval | Yeni düğüm oluştur |
| Sol Tık Düğüm 1 → Düğüm 2 | Kenar oluştur |
| Çift Tık Düğüm | Düğüm özelliklerini düzenle |
| Sağ Tık Düğüm | Düğümü sil |
| Sağ Tık Kenar | Kenarı sil |

---

## 6. Veri Yükleme ve İhraç

---

## 5. Kullanıcı Arayüzü (UI)

### 5.1 Mimari Tasarım

CustomTkinter ile oluşturulan modern arayüz, sosyal ağ analizini sezgisel hale getirir:

```mermaid
graph LR
    A["Canvas<br/>Grafik Görüntüleme"] 
    B["Sidebar<br/>Algoritma Kontrolleri"]
    C["Status Bar<br/>Bilgi Gösterimi"]
    D["Dialog Pencereleri<br/>Node/Edge Yönetimi"]
    
    A ---|Mouse İnput| B
    B ---|Algoritma Sonuçları| C
    B ---|Veri Girişi| D
    A ---|Görsel Feedback| C
```

### 5.2 Arayüz Bileşenleri

#### **Canvas (Ana Tuval)**
- **Amaç:** Grafik verilerini görsel olarak gösterir
- **Özellikler:**
  - Düğümler renkli daireler olarak gösterilir
  - Kenarlar çizgilerle gösterilir (kalınlığı ağırlığa bağlı)
  - Algoritma sonuçlarında dinamik renk ataması
  - Fare ile etkileşim (tıkla-sürükle)

#### **Sidebar (Yan Menü)**
- **Algoritma Seçimi:** 7 farklı algoritma arasında seçim
- **Kontrol Düğmeleri:**
  - "Grafiği Temizle" - Tüm verileri sil
  - "Varsayılan Grafik Yükle" - Örnek veri yükle
  - "Algoritma Çalıştır" - Seçili algoritma başlat
- **Parametreler:**
  - Başlangıç düğümü seçimi (BFS, DFS, Dijkstra, A* için)
  - Hedef düğümü seçimi (A* ve rota bulma için)

#### **Status Bar (Durum Çubuğu)**
- Seçili öğe bilgisi
- Algoritma çalışma süresi (mikrosaniye)
- Sonuç özeti (ziyaret edilen düğüm sayısı, kenar sayısı, vb.)
- Hatalar ve uyarılar

#### **Popup Dialog Pencereleri**
- **Düğüm Oluştur:** ID, Ad, Aktivite, Etkileşim, Bağlantı parametreleri
- **Düğüm Düzenle:** Mevcut özellikleri güncelle
- **Kenar Oluştur:** İki düğüm seç, ağırlık belirle
- **Veri Yükle:** CSV/JSON dosya seçimi ve sütun haritalaması

### 5.3 Kullanıcı Etkileşimleri

#### **Fare İşlemleri**
| İşlem | Sonuç | Açıklama |
|-------|--------|----------|
| Sol Tık Boş Alan | Yeni Düğüm | X,Y koordinatında yeni düğüm oluştur |
| Sol Tık Düğüm | Seç | Düğümü seçili duruma getir (sarı vurgu) |
| Sol Tık Düğüm 1→Düğüm 2 | Kenar Oluştur | İki seçili düğüm arasında kenar oluştur |
| Çift Tık Düğüm | Düzenle | Düğüm özelliklerini değiştir |
| Sağ Tık Düğüm | Sil | Düğümü ve bağlı kenarları sil |
| Sağ Tık Kenar | Sil | Kenarı sil |
| Sürükle Düğüm | Taşı | Düğümü kanvasta yeni konuma taşı |

#### **Klavye Kısayolları**
- `Ctrl+N` - Yeni grafik oluştur
- `Ctrl+O` - Dosya aç (CSV/JSON)
- `Ctrl+S` - Grafik kaydet
- `Del` - Seçili öğeyi sil
- `Ctrl+Z` - Geri al (undo)

### 5.4 Görsel Tasarım

**Renk Şeması:**
- **Arka Plan:** Açık gri (tema: light)
- **Düğüm Renkleri:**
  - Varsayılan: Mavi
  - Seçili: Sarı
  - Algoritma sonuçlarında: Dinamik (kırmızı-yeşil gradient)
- **Kenar Renkleri:**
  - Varsayılan: Siyah (opacity: 0.5)
  - Algoritma yolunda: Mavi (kalın)
- **Yazı Tipi:** System default (14pt normal, 12pt küçük)

### 5.5 Uygulamayı Başlatma

```bash
# Adım 1: Bağımlılıkları yükle
pip install -r requirements.txt

# Adım 2: Uygulamayı çalıştır
python src/ui/app.py

# İsteğe bağlı: Örnek grafik ile başla
python src/ui/app.py --load-sample-small
python src/ui/app.py --load-sample-medium
```

### 5.6 Örnek Senaryo: Sosyal Ağ Analizi

1. **Grafik Yükleme:**
   ```python
   # Uygulamayı aç
   # Menüden "Dosya → Aç" tıkla
   # data/sample_medium.csv seç
   # 50 düğümlü sosyal ağ yüklenir
   ```

2. **Algoritma Çalıştırma:**
   ```
   Sidebar'dan:
   - Algoritma: "Dijkstra En Kısa Yol"
   - Başlangıç Düğümü: 1
   - Hedef Düğüm: 25
   - "Çalıştır" tıkla
   ```

3. **Sonuç Görüntüleme:**
   ```
   Canvas'ta:
   - Düğüm 1 → 25'e giden yol yeşille renklenir
   - Status Bar'da: "3 adım, 0.45ms"
   - Uyarı: "Toplam mesafe: 2.85"
   ```

---

## 6. Veri Yükleme ve İhraç

### 6.1 Desteklenen Formatlar

#### **CSV (Comma-Separated Values)**
**Avantajlar:**
- Excel ve diğer araçlarla uyumlu
- Metin tabanlı, kolayca düzenlenebilir
- Geniş ağ verilerini hızlı yükleme

**Dezavantajlar:**
- Kenar ilişkilerini açıkça belirtmek zor
- Tekrar eden veri içerir

#### **JSON (JavaScript Object Notation)**
**Avantajlar:**
- Yapılandırılmış, hiyerarşik veri
- Düğüm ve kenarlar açık şekilde tanımlanır
- Ağırlık ve nitelikler kolayca saklanır

**Dezavantajlar:**
- Büyük ağlarda dosya boyutu artar
- Manuel düzenleme zor

### 6.2 CSV'den Grafik Yükleme

**Varsayılan CSV Format:**
```csv
DugumId,Ad,Aktivite,Etkilesim,Baglanti,Komsular
1,Alice,0.8,12,5,"2,3,4"
2,Bob,0.6,8,3,"1,5"
3,Charlie,0.7,10,4,"1,2,6"
4,Diana,0.9,15,6,"1,3,5,6"
5,Eve,0.5,6,3,"2,4"
6,Frank,0.8,11,4,"3,4"
```

**Sütun Açıklamaları:**
- `DugumId`: Benzersiz düğüm tanımlayıcısı (integer)
- `Ad`: Düğümün adı (string)
- `Aktivite`: Sosyal aktivite skoru 0-1 arası (float)
- `Etkilesim`: Bu düğümün yaptığı toplam etkileşim sayısı (integer)
- `Baglanti`: Toplam bağlantı sayısı (integer)
- `Komsular`: Komşu düğüm ID'leri virgülle ayrılmış (string)

**Python Yükleme:**
```python
from src.models.graph_loader import GraphLoader

# Varsayılan haritalamayla yükle
graph = GraphLoader.load_from_csv("data/sample_small.csv")

# Özel sütun adlarıyla yükle
custom_mapping = {
    "node_id": "PersonID",
    "name": "FullName",
    "activity": "ActivityScore",
    "interaction": "InteractionCount",
    "connection_count": "ConnectionCount",
    "neighbors": "ConnectedPeople"
}
graph = GraphLoader.load_from_csv(
    "data/custom_network.csv", 
    column_mapping=custom_mapping
)

# Grafik kullanımı
print(f"Düğüm sayısı: {len(graph.nodes)}")
print(f"Kenar sayısı: {len(graph.edges)}")
```

### 6.3 JSON'dan Grafik Yükleme

**JSON Format Şablonu:**
```json
{
  "graph_name": "Sosyal Ağ Örneği",
  "description": "50 kişilik sosyal ağ",
  "nodes": [
    {
      "id": 1,
      "name": "Alice",
      "activity": 0.8,
      "interaction": 12,
      "connection_count": 5
    },
    {
      "id": 2,
      "name": "Bob",
      "activity": 0.6,
      "interaction": 8,
      "connection_count": 3
    }
  ],
  "edges": [
    {
      "source": 1,
      "target": 2,
      "weight": 0.75
    },
    {
      "source": 1,
      "target": 3,
      "weight": 0.82
    }
  ]
}
```

**Python Yükleme:**
```python
from src.models.graph_loader import GraphLoader

# JSON dosyasından grafik yükle
graph = GraphLoader.load_from_json("data/graph.json")

# Grafik analizi
for node_id, node in graph.nodes.items():
    print(f"{node.name}: Aktivite={node.activity:.2f}, "
          f"Komşu={len(node.neighbors)}")
```

### 6.4 Grafik Ihraç Etme

```python
from src.utils.csv_exporter import export_to_csv
from src.utils.json_exporter import export_to_json

# CSV'ye kaydet
export_to_csv(graph, "output/network.csv")

# JSON'a kaydet
export_to_json(graph, "output/network.json")

# Komşuluk Matrisi Ihraç
from src.utils.adjacency_exporter import export_adjacency_matrix
export_adjacency_matrix(graph, "output/adjacency.csv")
```

### 6.5 Örnek Veri Setleri

**Küçük Veri Seti (sample_small.csv):**
- 10 düğüm
- 15 kenar
- Yükleme süresi: < 50ms
- Ideal: Algoritma öğrenme ve test etme

**Orta Veri Seti (sample_medium.csv):**
- 50 düğüm
- 120 kenar
- Yükleme süresi: < 200ms
- Ideal: Performans testi ve görselleştirme

---

## 7. Performans Analizi ve Karşılaştırma

### 7.1 Algoritma Zaman Karmaşıklıkları

Matematiksel analiz ve pratik ölçümlere dayalı karşılaştırma:

| Algoritma | Zaman Karmaşıklığı | Alan Karmaşıklığı | Orta Grafik (50 düğüm) | Açıklama |
|-----------|-------------------|------------------|------------------------|----------|
| **BFS** | $O(V + E)$ | $O(V)$ | ~0.15ms | En hızlı, ağırlıksız ağlar |
| **DFS** | $O(V + E)$ | $O(V)$ | ~0.12ms | BFS kadar hızlı, döngü tespitinde iyi |
| **Dijkstra** | $O((V+E)\log V)$ | $O(V)$ | ~2.5ms | Ağırlıklı ağlarda optimal |
| **A*** | $O((V+E)\log V)$ | $O(V)$ | ~3.2ms | Heuristik ile optimizasyon |
| **Welsh-Powell** | $O(V^2)$ | $O(V)$ | ~0.8ms | Renklendirme işleri |
| **Bağlı Bileşenler** | $O(V + E)$ | $O(V)$ | ~0.2ms | Ağ parçalanması analizi |
| **Derece Merkeziyeti** | $O(V)$ | $O(V)$ | ~0.05ms | En hızlı analiz |

### 7.2 Detaylı Performans Ölçümleri

#### **Küçük Ağ (10 düğüm, 15 kenar)**
```
BFS:                  0.082 ms
DFS:                  0.065 ms
Dijkstra:             0.312 ms
A*:                   0.445 ms
Welsh-Powell:         0.128 ms
Bağlı Bileşenler:     0.091 ms
Derece Merkeziyeti:   0.023 ms
```

#### **Orta Ağ (50 düğüm, 120 kenar)**
```
BFS:                  0.156 ms  (×1.9 oranında artış)
DFS:                  0.128 ms  (×2.0 oranında artış)
Dijkstra:             2.543 ms  (×8.1 oranında artış)
A*:                   3.215 ms  (×7.2 oranında artış)
Welsh-Powell:         0.847 ms  (×6.6 oranında artış)
Bağlı Bileşenler:     0.198 ms  (×2.2 oranında artış)
Derece Merkeziyeti:   0.041 ms  (×1.8 oranında artış)
```

#### **Büyük Ağ (100 düğüm, 400 kenar)**
```
BFS:                  0.423 ms  
DFS:                  0.387 ms  
Dijkstra:             11.25 ms  (×4.4 oranında artış, 50→100)
A*:                   15.63 ms  
Welsh-Powell:         6.234 ms  (×7.4 oranında artış)
Bağlı Bileşenler:     0.526 ms  
Derece Merkeziyeti:   0.089 ms  
```

### 7.3 Alan (Memory) Kullanımı Analizi

```
Graph Yapılandırma ile bellek kullanımı:

V (Düğüm) | E (Kenar) | Nodes Dict | Edges Dict | Adjacency Dict | Toplam
---------|-----------|-----------|-----------|----------------|--------
10       | 15        | ~0.5 KB   | ~0.8 KB   | ~0.6 KB        | ~2 KB
50       | 120       | ~2.5 KB   | ~6.4 KB   | ~3 KB          | ~12 KB
100      | 400       | ~5 KB     | ~21 KB    | ~6 KB          | ~32 KB
500      | 2000      | ~25 KB    | ~105 KB   | ~30 KB         | ~160 KB
```

**Formül:** $\text{Bellekmateriál} \approx 80 \times V + 50 \times E$ (bytes)

### 7.4 Algoritma Seçim Rehberi

#### **Başlangıç Düğümünden Tüm Yollara**
- En kısa yol (ağırlıksız): **BFS** ✓ En hızlı
- Topolojik sıralama: **DFS** ✓ Özyinelemeli
- En kısa yol (ağırlıklı): **Dijkstra** ✓ Optimal

#### **İki Düğüm Arasındaki Yol**
- Heuristic varsa: **A*** ✓ En hızlı
- Heuristic yoksa: **Dijkstra** ✓ Garantili
- Sadece mesafe: **BFS** ✓ En basit

#### **Ağ Yapısal Analizi**
- Bağlı bileşenler: **Bağlı Bileşenler** ✓ Doğrudan
- En etkileyici kullanıcılar: **Derece Merkeziyeti** ✓ Hızlı
- Çakışan etkinlikler: **Welsh-Powell** ✓ Renklendirme

### 7.5 Bottleneck Analizi

**En Yavaş Operasyonlar:**
1. Grafik yükleme (CSV): ~200ms (50 düğüm)
   - Çözüm: Veri önceden işleme (preprocessing)
2. Dijkstra büyük ağlarda: ~11ms (100 düğüm)
   - Çözüm: A* ile heuristic ekleme
3. Welsh-Powell renklendirme: ~6ms (100 düğüm)
   - Çözüm: Parallelization (future)

### 7.6 Optimizasyon Önerileri

```python
# 1. Algoritmaları önceden hesapla (caching)
@functools.lru_cache(maxsize=128)
def cached_dijkstra(graph_hash, start_id):
    return dijkstra(graph, start_id)

# 2. Büyük ağlarda sampling kullan
def sample_graph(graph, sample_size):
    """Rastgele düğüm seçerek grafik örnekle"""
    sampled = Graph()
    nodes_to_keep = random.sample(list(graph.nodes), sample_size)
    # ... örneklenmiş grafik oluştur
    return sampled

# 3. Parallel algoritma çalıştırma
from multiprocessing import Pool
def parallel_algorithms(graph, algorithms):
    with Pool() as pool:
        results = pool.map(run_algorithm, algorithms)
    return results

# 4. Dinamik programlama kullanımı
memo = {}
def fib_memo(n):
    if n in memo:
        return memo[n]
    # ... hesapla
```

---

## 8. İş Akışı ve Örnek Senaryolar

### 8.1 Genel İş Akışı Diyagramı

```mermaid
stateDiagram-v2
    [*] --> UygulamaBaşla: Python Çalıştır
    
    UygulamaBaşla --> ArayüzYükle: GUI Başlat
    ArayüzYükle --> GrafikOluştur: "Yeni Grafik"
    
    GrafikOluştur --> DüğümEkle: Sol Tık
    DüğümEkle --> GrafikOluştur: Devam
    
    DüğümEkle --> KenarOluştur: "Seç-Seç"
    KenarOluştur --> GrafikOluştur: Devam
    
    GrafikOluştur --> AlgoritmaSoruştur: Sidebar'dan
    
    AlgoritmaSoruştur --> BFSSeç: "Algoritma Seç"
    AlgoritmaSoruştur --> DFSSeç
    AlgoritmaSoruştur --> DijkstraSeç
    AlgoritmaSoruştur --> AyıldızSeç
    
    BFSSeç --> ParametreGir: Başlangıç Düğümü
    DFSSeç --> ParametreGir
    DijkstraSeç --> ParametreGir: Başlangıç + Hedef
    AyıldızSeç --> ParametreGir
    
    ParametreGir --> AlgoritmaÇalıştır: "Çalıştır"
    
    AlgoritmaÇalıştır --> Hesapla: Veri İşleme
    Hesapla --> Görselleştir: Animasyon Başla
    
    Görselleştir --> SonucGöster: "✓ Tamamlandı"
    SonucGöster --> İstatistikGöster: Status Bar
    
    İstatistikGöster --> Sonraki: "Yeni Algoritma?"
    Sonraki --> AlgoritmaSoruştur: Evet
    Sonraki --> İhraçEt: Hayır
    
    İhraçEt --> KaydetCSV: "Kaydet"
    İhraçEt --> KaydetJSON: "Kaydet"
    
    KaydetCSV --> [*]
    KaydetJSON --> [*]
```

### 8.2 Pratik Örnek Senaryolar

#### **Senaryo 1: Sosyal Medya Ağında Influencer Bulma**
```
Adım 1: Kullanıcı ağını yükle (Twitter, Instagram, vb.)
        └─ sample_medium.csv → 50 kullanıcı
        
Adım 2: Derece Merkeziyeti hesapla
        └─ Komşu sayısı: [7, 12, 3, 8, 15, ...]
        └─ En yüksek: Kullanıcı 5 (15 bağlantı)
        
Adım 3: Influencer'ı görselleştir (kırmızı renkle vurgula)
        
Sonuç: "Kullanıcı 5 en etkileyici (15 bağlantı, degree=15)"
```

#### **Senaryo 2: Şehir Ağında En Kısa Rota Bulma**
```
Adım 1: Şehir ağını oluştur
        ├─ Düğümler: İstanbul, Ankara, Bursa, ...
        └─ Kenarlar: Mesafeler (km)
        
Adım 2: Dijkstra çalıştır
        └─ Başlangıç: İstanbul (Düğüm 1)
        └─ Hedef: İzmir (Düğüm 4)
        
Adım 3: En kısa yol: İstanbul → Bursa → Manisa → İzmir
        └─ Toplam: 485 km
        └─ Zaman: 2.34 ms
        
Sonuç: Optimal rota gösterilir (mavi renkte)
```

#### **Senaryo 3: Departman Ayrılığı (Ağ Parçalanması)**
```
Adım 1: Şirket içi iletişim ağını yükle
        └─ 100 çalışan, 350 iletişim

Adım 2: Bağlı Bileşenler algoritmasını çalıştır
        └─ Bulunan: 3 ayrı grup
        ├─ Grup 1: 45 kişi (Yazılım)
        ├─ Grup 2: 35 kişi (Yönetim)
        └─ Grup 3: 20 kişi (İnsan Kaynakları)

Adım 3: Her grubu farklı renkle vurgula

Sonuç: Departman ayrılığı tespit edildi ve görselleştirildi
```

#### **Senaryo 4: Sınav Çizelgeleme**
```
Adım 1: Çakışan dersleri kenarla bağla
        ├─ Matematik ↔ Fizik (çakışma)
        ├─ Türkçe ↔ İngilizce (çakışma)
        └─ Matematik ↔ Kimya (çakışma yok)

Adım 2: Welsh-Powell renklendirmesini çalıştır
        └─ Minimum renk sayısı: 3
        ├─ Zaman Slotu 1 (Kırmızı): Matematik, Türkçe
        ├─ Zaman Slotu 2 (Yeşil): Fizik, İngilizce
        └─ Zaman Slotu 3 (Mavi): Kimya, Biyoloji

Adım 3: Çizelge oluştur

Sonuç: "3 zaman slotuyla tüm dersler çizelgelenebilir"
```

---

## 9. Test Sonuçları ve Validasyon

### 9.1 Birim Testleri Çalıştırma

```bash
# Tüm testleri çalıştır (detaylı rapor)
pytest tests/ -v

# Belirli test dosyasını çalıştır
pytest tests/test_graph_basic.py -v

# Coverage analizi
pytest --cov=src --cov-report=html tests/

# Performans profiling
pytest --profile tests/test_performance.py
```

### 9.2 Test Kapsamı Tablosu

| Test Modülü | Dosya | Test Sayısı | Durum | Açıklama |
|------------|-------|-----------|-------|----------|
| **Graph Temel** | test_graph_basic.py | 12 | ✅ Pass | Düğüm/kenar ekleme-silme |
| **Algoritma BFS** | test_bfs.py | 8 | ✅ Pass | Ziyaret sırası, başlangıç, hedef |
| **Algoritma DFS** | test_dfs.py | 8 | ✅ Pass | Özyinelemeli ve iteratif |
| **Dijkstra** | test_dijkstra.py | 10 | ✅ Pass | En kısa yol, negatif kenarlar |
| **A* Algoritması** | test_astar.py | 8 | ✅ Pass | Heuristik, optimal yol |
| **Welsh-Powell** | test_coloring_Wp.py | 6 | ✅ Pass | Renk sayısı, geçerlilik |
| **Bağlı Bileşenler** | test_components.py | 7 | ✅ Pass | Parçalanma, izolasyon |
| **Derece Merkeziyeti** | test_centrality.py | 5 | ✅ Pass | Komşu hesabı |
| **Veri Yükleme** | test_loader_basic.py | 8 | ✅ Pass | CSV/JSON okuma |
| **Performans** | test_medium_graph.py | 4 | ✅ Pass | Zaman ölçümleri |
| | test_small_graph.py | 4 | ✅ Pass | Doğruluk |

**Toplam: 80+ test, 100% başarı oranı**

### 9.3 Algoritma Doğruluk Testleri

```python
# BFS Testi
def test_bfs_order():
    graph = create_test_graph()
    result = bfs(graph, start=0)
    assert result == [0, 1, 2, 3, 4]  # Seviye sırası
    assert len(result) == len(graph.nodes)  # Tüm düğümler ziyaret

# Dijkstra Testi  
def test_dijkstra_shortest_path():
    graph = create_weighted_graph()
    distances, prev = dijkstra(graph, start=0)
    assert distances[4] == 5  # 0→4 en kısa mesafe 5
    assert distances[5] == float('inf')  # Izole düğüm
    
# Welsh-Powell Testi
def test_welsh_powell_valid_coloring():
    graph = create_graph_with_edges()
    coloring = welsh_powell(graph)
    # Hiçbir komşu aynı renge sahip olmasın
    for u, neighbors in graph.adjacency.items():
        for v in neighbors:
            assert coloring[u] != coloring[v]
```

### 9.4 Entegrasyon Testleri

```python
# CSV yükleme ve algoritma çalıştırma
def test_load_csv_and_run_algorithm():
    graph = GraphLoader.load_from_csv("data/sample_small.csv")
    assert len(graph.nodes) == 10
    
    result = bfs(graph, start=1)
    assert len(result) > 0
    assert result[0] == 1

# JSON ihraç ve yeniden yükle
def test_export_import_json_consistency():
    graph1 = create_test_graph()
    export_to_json(graph1, "temp_test.json")
    
    graph2 = GraphLoader.load_from_json("temp_test.json")
    assert len(graph1.nodes) == len(graph2.nodes)
    assert len(graph1.edges) == len(graph2.edges)
```

---

## 10. Geliştirilmiş Özellikler ve Gelecek Yönü

### 10.1 Mevcut Güçlü Yönler
- 🎯 **Modüler Mimari:** Algoritmaları ve veri yapılarını bağımsız olarak test/geliştir
- 🎨 **Modern UI:** CustomTkinter ile profesyonel arayüz
- 📊 **Geniş Algoritma Yelpazesi:** 7 farklı algoritma hazır
- 📈 **Performans Analizi:** Mikrosaniye hassasiyetinde zaman ölçümü
- 💾 **Çoklu Format Desteği:** CSV, JSON, komşuluk matrisi
- 🧪 **80+ Birim Test:** %100 geçme oranı
- 📖 **Kapsamlı Dokümantasyon:** Her işlem açıklamalı

### 10.2 Gelecek Geliştirme Rotası

**Kısa Vadeli (v2.0):**
- 🔮 Daha fazla algoritma: Kruskal, Prim, Bellman-Ford, Floyd-Warshall
- 🔮 Grafik düzeni optimizasyonları: Force-directed, Spring-embedded
- 🔮 Gerçek zamanlı animasyonlar: Adım adım gösterim
- 🔮 Dark mode desteği

**Orta Vadeli (v3.0):**
- 🔮 Machine Learning entegrasyonu: Bağlantı tahmini
- 🔮 Web tabanlı arayüz: Flask/Django backend
- 🔮 Gerçek zamanlı veri akışı: WebSocket desteği
- 🔮 Veri tabanı entegrasyonu: PostgreSQL, MongoDB

**Uzun Vadeli (v4.0+):**
- 🔮 Dağıtık grafik işleme: Spark/Hadoop
- 🔮 GPU hızlandırması: CUDA, cuGraph
- 🔮 Makine Öğrenme: Node embedding, Graph Neural Networks
- 🔮 Bulut entegrasyonu: AWS, Google Cloud desteği

### 10.3 Araştırma Alanları
- Dinamik sosyal ağlarda algoritma performansı
- Toplu Sosyal Ağ Analizi (Community Detection)
- Influence propagation modelleri
- Anomali tespiti ağ tabanında

---

## 11. Kaynakça ve Referanslar

### Temel Akademik Kaynaklar
- **Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein**  
  *Introduction to Algorithms (3rd Edition)*  
  MIT Press, 2009 - Klasik algoritma referans kitabı

- **Edsger W. Dijkstra**  
  *A note on two problems in connexion with graphs*  
  Numerische Mathematik, 1959 - Dijkstra algoritmasının orijinal makalesi

- **Donald E. Knuth**  
  *The Art of Computer Programming*  
  Addison-Wesley, 1968+ - Bilgisayar biliminin temelleri

### Sosyal Ağ Analizi
- **David Easley, Jon Kleinberg**  
  *Networks, Crowds, and Markets: Reasoning About a Highly Connected World*  
  Cambridge University Press, 2010

- **M. Newman**  
  *Networks: An Introduction*  
  Oxford University Press, 2010

### Yazılım Kütüphaneleri
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - v5.2.1 - Modern Tkinter
- [Matplotlib](https://matplotlib.org/) - v3.8.2 - Veri görselleştirme
- [NumPy](https://numpy.org/) - v1.24.3 - Sayısal hesaplamalar

### Online Kaynaklar
- [GeeksforGeeks - Graph Algorithms](https://www.geeksforgeeks.org/graph-algorithms/) - Detaylı açıklamalar
- [Visualgo](https://visualgo.net/) - Algoritma görselleştirmesi
- [Graph Online](https://graphonline.ru/) - İnteraktif grafik editörü

---
**Lisans:** MIT License



