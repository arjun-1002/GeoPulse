/**
 * Kerala Tourism Intelligence - Executive Dashboard Engine
 * Handles interactive mapping (Leaflet), Chart.js visual analytics,
 * destination state synchronization, sorting, and dynamic insight generation.
 */

(function () {
  'use strict';

  // 1. Data Ingestion from Flask Context
  const rawData = window.KERALA_DATA || {};
  const master = rawData.master || [];
  const seasonal = rawData.seasonal || [];
  const opportunities = rawData.opportunities || [];
  const clusters = rawData.clusters || [];
  const clusterSummary = rawData.cluster_summary || [];
  const destinations = rawData.destinations || [];

  // Active state
  let currentDestination = destinations[0] || 'Munnar';
  let activeSeasonalityMode = 'index'; // 'index' or 'interest'
  let leafletMap = null;
  let mapMarkers = {};
  let currentSort = { column: 'Visits_Per_Cafe', order: 'desc' };

  // Home Page Specific State & Chart instances
  let homeMiniMap = null;
  let homeMiniMarkers = {};
  let chartHomeTrend = null;
  let chartHomeLandscape = null;
  let homeTrendMode = '3years';
  let showAllHomePills = false;

  // Deep Dive & Comparator Chart instances
  let chartSeasonality = null;
  let chartAccomDonut = null;
  let chartCompareBar = null;
  let chartCompareSeason = null;

  // 2. Comprehensive Destination Metadata Registry with Kerala Cultural Identity
  const DESTINATION_META = {
    Munnar: {
      district: 'Idukki',
      category: 'hill',
      categoryLabel: 'Hill Station & Tea Corridors',
      keralaTag: 'Neelakurinji Highlands • Kannan Devan Tea Terraces',
      lat: 10.0889,
      lng: 77.0595,
      photo: 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=150&q=80',
      desc: 'Iconic highland plateau carpeted with emerald tea plantations, cool misty climate, and dramatic peak-season surges.'
    },
    Wayanad: {
      district: 'Wayanad',
      category: 'hill',
      categoryLabel: 'Highland Rainforest & Eco-Reserves',
      keralaTag: 'Edakkal Caves & Chembra Peak Sanctuary',
      lat: 11.605,
      lng: 76.0828,
      photo: 'https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=150&q=80',
      desc: 'Biodiverse high-altitude sanctuary celebrated for mist-clad peaks, wildlife sanctuaries, and expanding plantation retreats.'
    },
    Vagamon: {
      district: 'Idukki',
      category: 'hill',
      categoryLabel: 'Pine Forests & Rolling Meadows',
      keralaTag: 'Pine Corridors & Paragliding Valley',
      lat: 9.6894,
      lng: 76.9064,
      photo: 'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=150&q=80',
      desc: 'Serene offbeat hill station renowned for grassy knolls, pine valleys, and emerging adventure/paragliding tourism.'
    },
    Thekkady: {
      district: 'Idukki',
      category: 'hill',
      categoryLabel: 'Periyar Tiger Reserve & Spice Corridors',
      keralaTag: 'Periyar Wildlife & Spice Country',
      lat: 9.6031,
      lng: 77.1665,
      photo: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=150&q=80',
      desc: 'Premier wildlife destination wrapped around Periyar Lake with rich spice plantations and international wildlife interest.'
    },
    Alappuzha: {
      district: 'Alappuzha',
      category: 'backwaters',
      categoryLabel: 'Venice of the East & Houseboat Network',
      keralaTag: 'Kettuvallam & Houseboat Corridors',
      lat: 9.4981,
      lng: 76.3388,
      photo: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=150&q=80',
      desc: 'The heart of Kerala backwater cruising with vast canal networks, paddy waterways, and traditional kettuvallam houseboats.'
    },
    Kumarakom: {
      district: 'Kottayam',
      category: 'backwaters',
      categoryLabel: 'Vembanad Lake & Luxury Lagoons',
      keralaTag: 'Vembanad Lake & Bird Sanctuary',
      lat: 9.6175,
      lng: 76.4301,
      photo: 'https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=150&q=80',
      desc: 'Prestigious luxury eco-resort cluster on Vembanad Lake, home to a world-renowned migratory bird sanctuary.'
    },
    Varkala: {
      district: 'Thiruvananthapuram',
      category: 'coastal',
      categoryLabel: 'Red Laterite Cliffs & Bohemian Coast',
      keralaTag: 'Red Laterite Cliffs & Surf Shore',
      lat: 8.7379,
      lng: 76.7163,
      photo: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=150&q=80',
      desc: 'Dramatic geological red cliff coastline with beachside cafes, international surfing culture, and wellness retreats.'
    },
    Kovalam: {
      district: 'Thiruvananthapuram',
      category: 'coastal',
      categoryLabel: 'Crescent Beaches & Lighthouse Bay',
      keralaTag: 'Lighthouse Beach & Ayurvedic Haven',
      lat: 8.4004,
      lng: 76.9787,
      photo: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=150&q=80',
      desc: 'Internationally recognized beach haven famous for its striped coastal lighthouse, calm bathing bays, and Ayurvedic centers.'
    },
    Kochi: {
      district: 'Ernakulam',
      category: 'urban',
      categoryLabel: 'Colonial Port & Commercial Metro',
      keralaTag: 'Chinese Fishing Nets & Spice Gateway',
      lat: 9.9312,
      lng: 76.2673,
      photo: 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=150&q=80',
      desc: 'The economic nerve-center and cultural capital of Kerala, merging ancient maritime history with booming modern commerce.'
    },
    Kozhikode: {
      district: 'Kozhikode',
      category: 'urban',
      categoryLabel: 'Historic Malabar & Gastronomy Capital',
      keralaTag: 'Sweet Meat Street & UNESCO Literature Port',
      lat: 11.2588,
      lng: 75.7804,
      photo: 'https://images.unsplash.com/photo-1500534623283-312aaded485b?auto=format&fit=crop&w=1200&q=80',
      thumb: 'https://images.unsplash.com/photo-1500534623283-312aaded485b?auto=format&fit=crop&w=150&q=80',
      desc: 'Historic Malabar trading port and UNESCO City of Literature, celebrated worldwide for its unparalleled culinary heritage.'
    }
  };

  // Comprehensive Precomputed Opportunity & Insights Data Registry
  const OPPORTUNITY_DATA = {
    Munnar: {
      score: 82,
      checks: ['Strong Tourist Interest', 'Growing Visitor Count (+181%)', 'Rank #1 Cafe & Dining Deficit'],
      opportunities: [
        { title: 'Homestays & Boutique Stays', desc: 'High demand, limited supply', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Cafes & Specialty Bistros', desc: 'Severe deficit: 28K visits/cafe', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Trekking & Tea Trail Tours', desc: 'Rising interest in eco-trails', tag: 'Medium', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Munnar shows strong search interest across India, surging 181% by 2025.',
        'Tourism demand peaks sharply during Oct – Mar holiday windows.',
        'High commercial scope in specialty cafes, boutique stays, and plantation retreats.'
      ]
    },
    Wayanad: {
      score: 76,
      checks: ['High Eco-Tourism Demand', 'Stable 590K+ Annual Visitors', 'Emerging Specialty Dining Corridor'],
      opportunities: [
        { title: 'Eco-Resorts & Treehouse Stays', desc: 'Expanding forest plantation retreats', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Farm-to-Table Gastronomy', desc: 'Growing culinary leisure demand', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Wildlife & Adventure Safaris', desc: 'High interest in Chembra & Kabini', tag: 'Medium', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Wayanad serves as northern Kerala’s prime weekend getaway for Bengaluru and Mysuru travelers.',
        'Search interest remains steady throughout monsoon and peaks in Dec.',
        'Great opportunity for eco-certified stays and artisanal coffee retreats.'
      ]
    },
    Vagamon: {
      score: 79,
      checks: ['Fastest Growing Offbeat Station', 'Rank #3 Cafe Supply Deficit', 'Emerging Adventure & Paragliding Hub'],
      opportunities: [
        { title: 'Glamping & Hill Cottages', desc: 'Limited lodging footprint (33 stays)', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Scenic Valley Cafes', desc: '13.9K visits/cafe, high deficit', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Paragliding & Outdoor Camps', desc: 'Leading paragliding spot in South India', tag: 'Medium', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Vagamon attracts younger demographic and road-trippers seeking uncrowded landscapes.',
        'Pronounced demand spikes during long weekends and summer holidays.',
        'Substantial opportunity for boutique experiential glamping and scenic cafes.'
      ]
    },
    Thekkady: {
      score: 86,
      checks: ['Acute Lodging Bottleneck (Rank #3)', 'High Dining Pressure (Rank #2)', '79K+ Foreign Visitors Annually'],
      opportunities: [
        { title: 'Boutique Jungle Lodges', desc: '12.4K visits/stay; tight inventory', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Specialty Cafes & Spice Bistros', desc: '17.3K visits/cafe; Rank #2 gap', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Guided Spice & Wildlife Safaris', desc: 'High international traveler footfall', tag: 'Medium', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Thekkady attracts the highest ratio of international travelers among inland destinations.',
        'Experiences acute commercial deficit with only 46 stays and 33 cafes recorded.',
        'Stable demand anchored by Periyar Tiger Reserve ecotourism.'
      ]
    },
    Alappuzha: {
      score: 74,
      checks: ['Iconic Backwater Cruising Hub', '620K+ Baseline Annual Visitors', 'High Canalfront Dining Scope'],
      opportunities: [
        { title: 'Eco-Luxury Solar Houseboats', desc: 'Green transition in backwater cruising', tag: 'High', img: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=160&q=80' },
        { title: 'Waterfront Heritage Dining', desc: 'High evening visitor concentration', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Canal Kayaking & Village Stays', desc: 'Rising demand for slow experiential travel', tag: 'Medium', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Alappuzha is Kerala’s globally recognized signature backwater gateway.',
        'Peak season in December surges to 123.5% of annual baseline demand.',
        'Scope for premium canalfront gastronomy and eco-compliant cruise vessels.'
      ]
    },
    Kumarakom: {
      score: 77,
      checks: ['Ultra-Luxury Lagoon Segment', 'High Foreign Visitor Spend', 'Rank #4 Specialty Cafe Deficit'],
      opportunities: [
        { title: 'Ayurveda & Wellness Retreats', desc: 'High-margin rejuvenation retreats', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Lakeside Artisanal Cafes', desc: '12.3K visits/cafe, tight cafe supply', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Destination Wedding Venues', desc: 'Surging luxury lakefront events', tag: 'Medium', img: 'https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Kumarakom commands the highest room yields and luxury resort concentration in Kerala.',
        'Significant deficit in casual specialty cafes and boutique dining for day-trippers.',
        'High international guest satisfaction on Vembanad Lake.'
      ]
    },
    Varkala: {
      score: 81,
      checks: ['Surging Coastal Footfall (+90%)', 'Rank #4 Stay Deficit (12K/stay)', 'Digital Nomad & Surfing Inflow'],
      opportunities: [
        { title: 'Cliffside Co-Living & Hostels', desc: '12K visits/stay; tight budget boutique supply', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Surf Schools & Beach Clubs', desc: 'Emerging surf capital of South India', tag: 'High', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=160&q=80' },
        { title: 'Sunset Lounges & Organic Cafes', desc: 'Vibrant nomad and backpacker market', tag: 'Medium', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Varkala recorded massive growth, reaching 707K+ annual domestic visitors in 2025.',
        'Accommodation supply remains constrained at just 31 recorded listings.',
        'Strongest digital nomad and wellness traveler appeal along the southern coastline.'
      ]
    },
    Kovalam: {
      score: 73,
      checks: ['Established International Beach Brand', '630K+ Annual Footfall', 'High Rejuvenation & Wellness Base'],
      opportunities: [
        { title: 'Premium Beachfront Stays', desc: 'Steady domestic and foreign demand', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Specialty Coastal Seafood Dining', desc: 'High tourist turnover along promenade', tag: 'Medium', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' },
        { title: 'Yoga & Panchakarma Centers', desc: 'Established European and global clientele', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Kovalam is Kerala’s heritage beach resort corridor with 61K+ foreign visitors.',
        'Seasonality peaks from October through February.',
        'Opportunity for upgraded boutique hospitality and upscale wellness facilities.'
      ]
    },
    Kochi: {
      score: 88,
      checks: ['Massive 3M+ Footfall & Gateway Hub', 'Rank #2 Lodging Deficit (13K/stay)', 'Highest Commercial Liquidity'],
      opportunities: [
        { title: 'Heritage Boutique Stays (Fort Kochi)', desc: 'High room rates and year-round occupancy', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Business & MICE Hotels', desc: 'Steady corporate and international transit', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Artisanal Cafes & Nightlife Concepts', desc: 'Massive culinary volume (1,641 restaurants)', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Kochi represents Kerala’s largest urban and commercial tourism gateway (3M domestic, 198K foreign).',
        'Despite 201 hotels, ratio of 13,087 visits per stay indicates immense lodging demand.',
        'Highest year-round stability with Biennale and MICE conferencing.'
      ]
    },
    Kozhikode: {
      score: 84,
      checks: ['Most Acute Stay Shortage (Rank #1)', 'UNESCO City of Literature & Food Capital', 'High Transit & Culinary Tourism'],
      opportunities: [
        { title: 'Mid-Market & Business Hotels', desc: 'Severe shortage: 22.4K visits per stay (Rank #1)', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Heritage Coastal Homestays', desc: 'Growing leisure and cultural interest', tag: 'High', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=160&q=80' },
        { title: 'Signature Culinary & Dessert Concepts', desc: 'Celebrated Malabar culinary hub', tag: 'High', img: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=160&q=80' }
      ],
      insights: [
        'Kozhikode has the most extreme accommodation bottleneck in Kerala with 22,458 visits per stay.',
        'World-famous Malabar culinary tourism drives heavy domestic visitor inflows.',
        'Huge gap for quality boutique business hotels and curated heritage stays.'
      ]
    }
  };

  // 3. Helper Functions for Fuzzy Column Matching & Formatting
  function findCol(row, candidates) {
    if (!row) return null;
    const keys = Object.keys(row);
    for (let c of candidates) {
      const match = keys.find(k => k.toLowerCase().replace(/[ _]/g, '') === c.toLowerCase().replace(/[ _]/g, ''));
      if (match) return match;
    }
    for (let c of candidates) {
      const match = keys.find(k => k.toLowerCase().replace(/[ _]/g, '').includes(c.toLowerCase().replace(/[ _]/g, '')));
      if (match) return match;
    }
    return null;
  }

  function getVal(row, candidates, fallback = 0) {
    const key = findCol(row, candidates);
    if (!key || row[key] === null || row[key] === undefined || row[key] === '') return fallback;
    const num = Number(row[key]);
    return isNaN(num) ? fallback : num;
  }

  function fmtNumber(n) {
    return Number(n || 0).toLocaleString('en-IN');
  }

  function fmtCompact(n) {
    const num = Number(n || 0);
    if (num >= 10000000) return (num / 10000000).toFixed(1) + ' Cr';
    if (num >= 100000) return (num / 100000).toFixed(1) + ' Lakh';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
    return String(num);
  }

  function getMasterRow(destName) {
    return master.find(r => String(r.Destination || r.destination || '').trim().toLowerCase() === destName.trim().toLowerCase()) || {};
  }

  function getOpportunityRow(destName) {
    return opportunities.find(r => String(r.Destination || r.destination || '').trim().toLowerCase() === destName.trim().toLowerCase()) || {};
  }

  function getClusterRow(destName) {
    return clusters.find(r => String(r.Destination || r.destination || '').trim().toLowerCase() === destName.trim().toLowerCase()) || {};
  }

  function getSeasonalRows(destName) {
    return seasonal.filter(r => String(r.destination || r.Destination || '').trim().toLowerCase() === destName.trim().toLowerCase());
  }

  // 4. Initial UI Setup & Navigation Handlers
  function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section-pane');
    const breadcrumb = document.getElementById('activeBreadcrumb');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');

    function setActiveTab(targetId) {
      const targetNav = targetId.replace('#', '');
      navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.nav === targetNav);
      });

      sections.forEach(sec => {
        sec.classList.toggle('active', sec.id === targetNav);
      });

      const activeLink = document.querySelector(`.nav-link[data-nav="${targetNav}"] span`);
      if (activeLink && breadcrumb) {
        breadcrumb.textContent = activeLink.textContent;
      }

      // Close mobile sidebar if open
      if (sidebar) sidebar.classList.remove('open');

      // Scroll to top of window smoothly
      window.scrollTo({ top: 0, behavior: 'smooth' });

      // Trigger Leaflet map invalidateSize if navigating to overview
      if (targetNav === 'overview' && leafletMap) {
        setTimeout(() => leafletMap.invalidateSize(), 200);
      }
    }

    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const hash = link.getAttribute('href');
        if (hash && hash.startsWith('#')) {
          e.preventDefault();
          window.location.hash = hash;
          setActiveTab(hash);
        }
      });
    });

    window.addEventListener('hashchange', () => {
      if (window.location.hash) {
        setActiveTab(window.location.hash);
      }
    });

    if (window.location.hash) {
      setActiveTab(window.location.hash);
    }

    if (sidebarToggleBtn && sidebar) {
      sidebarToggleBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
    }

    if (sidebarCloseBtn && sidebar) {
      sidebarCloseBtn.addEventListener('click', () => sidebar.classList.remove('open'));
    }

    // Theme Toggle
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeLabel = document.getElementById('themeToggleLabel');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const isDark = document.body.classList.toggle('theme-dark');
        document.body.classList.toggle('theme-light', !isDark);
        if (themeLabel) themeLabel.textContent = isDark ? 'Light Theme' : 'Dark Theme';
        try { localStorage.setItem('kt_theme', isDark ? 'dark' : 'light'); } catch (e) {}
      });

      try {
        if (localStorage.getItem('kt_theme') === 'dark') {
          document.body.classList.add('theme-dark');
          document.body.classList.remove('theme-light');
          if (themeLabel) themeLabel.textContent = 'Light Theme';
        }
      } catch (e) {}
    }

    // Print Report
    const printBtn = document.getElementById('printReportBtn');
    if (printBtn) {
      printBtn.addEventListener('click', () => window.print());
    }
  }

  // 5. Global Search & Archetype Filters
  function initSearchAndFilters() {
    const searchInput = document.getElementById('globalSearchInput');
    const clearBtn = document.getElementById('clearSearchBtn');
    const filterChips = document.querySelectorAll('.filter-chip');

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim().toLowerCase();
        if (clearBtn) clearBtn.style.display = query ? 'block' : 'none';

        const match = destinations.find(d => d.toLowerCase() === query);
        if (match) {
          selectDestination(match);
        }
      });

      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const query = searchInput.value.trim().toLowerCase();
          const match = destinations.find(d => d.toLowerCase().includes(query));
          if (match) {
            selectDestination(match);
          }
        }
      });
    }

    if (clearBtn && searchInput) {
      clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearBtn.style.display = 'none';
        searchInput.focus();
      });
    }

    // Filter Chips
    filterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        filterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const filter = chip.dataset.filter;
        renderDestQuickList(filter);
        highlightMapCategory(filter);
      });
    });
  }

  // 6. Interactive Leaflet Map of Kerala
  function initLeafletMap() {
    const mapContainer = document.getElementById('keralaLeafletMap');
    if (!mapContainer) return;

    if (typeof L === 'undefined') {
      mapContainer.innerHTML = `
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color:#64748b; text-align:center; padding:24px; background:#f0fdf4;">
          <span style="font-size:32px; margin-bottom:8px;">🗺️</span>
          <strong style="font-size:15px; color:#064e3b; margin-bottom:4px;">Kerala Geographic Explorer</strong>
          <p style="font-size:12px; max-width:320px;">Interactive map tiles connect via Leaflet. You can select any of the 10 benchmark destinations from the roster on the right or the tabs above.</p>
        </div>
      `;
      return;
    }

    try {
      leafletMap = L.map('keralaLeafletMap', {
        center: [10.25, 76.45],
        zoom: 7.4,
        zoomSnap: 0.1,
        scrollWheelZoom: false,
        attributionControl: false
      });

      // OpenStreetMap tiles for clean, reliable cartography without watermark
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap'
      }).addTo(leafletMap);

      // Render markers for all 10 destinations
      destinations.forEach(name => {
        const meta = DESTINATION_META[name];
        if (!meta) return;

        const mRow = getMasterRow(name);
        const visits = getVal(mRow, ['Domestic_Visits_2022', 'Domestic_Visits']);

        // Custom HTML Marker Icon
        const iconHtml = `
          <div class="custom-dest-pin ${meta.category}" title="${name}">
            <span>${name.substring(0, 2).toUpperCase()}</span>
          </div>
        `;

        const customIcon = L.divIcon({
          className: 'custom-leaflet-marker',
          html: iconHtml,
          iconSize: [32, 32],
          iconAnchor: [16, 16]
        });

        const marker = L.marker([meta.lat, meta.lng], { icon: customIcon }).addTo(leafletMap);
        mapMarkers[name] = marker;

        // Popup with rich information
        const popupContent = `
          <div style="font-family:'Plus Jakarta Sans',sans-serif; min-width: 170px; padding: 2px;">
            <strong style="font-size:14px; color:#064e3b; display:block; font-family:'Outfit',sans-serif;">${name}</strong>
            <span style="font-size:11px; color:#64748b; display:block; margin-bottom:6px;">${meta.district} District</span>
            <div style="font-size:11.5px; line-height:1.5;">
              <div>👥 <b>${fmtNumber(visits)}</b> visits</div>
              <div>🏨 <b>${getVal(mRow, ['Total_Accommodation_Listings'])}</b> stays</div>
              <div>🍽 <b>${getVal(mRow, ['Restaurants']) + getVal(mRow, ['Cafes'])}</b> dining listings</div>
            </div>
            <button onclick="window.selectKeralaDest('${name}', true)" style="margin-top:8px; width:100%; background:#059669; color:#fff; border:none; border-radius:6px; padding:4px 8px; font-size:11px; font-weight:700; cursor:pointer;">
              Inspect 360° Profile →
            </button>
          </div>
        `;

        marker.bindPopup(popupContent);

        marker.on('click', () => {
          updateMapOverlay(name);
          selectDestination(name, false);
        });

        marker.on('mouseover', () => {
          updateMapOverlay(name);
        });
      });

      // Overlay Inspect Button
      const overlayInspectBtn = document.getElementById('overlayInspectBtn');
      if (overlayInspectBtn) {
        overlayInspectBtn.addEventListener('click', () => {
          selectDestination(currentDestination, true);
        });
      }

    } catch (err) {
      console.warn('Leaflet map initialization warning:', err);
    }
  }

  function updateMapOverlay(destName) {
    const meta = DESTINATION_META[destName];
    const mRow = getMasterRow(destName);
    if (!meta) return;

    const overlay = document.getElementById('mapFloatingOverlay');
    const title = document.getElementById('overlayDestTitle');
    const metaEl = document.getElementById('overlayDestMeta');
    const visits = document.getElementById('overlayVisits');
    const stays = document.getElementById('overlayStays');
    const cafes = document.getElementById('overlayCafes');

    if (title) title.textContent = destName;
    if (metaEl) metaEl.textContent = `${meta.district} District • ${meta.categoryLabel}`;
    if (visits) visits.textContent = fmtCompact(getVal(mRow, ['Domestic_Visits_2022', 'Domestic_Visits']));
    if (stays) stays.textContent = fmtNumber(getVal(mRow, ['Total_Accommodation_Listings']));
    if (cafes) cafes.textContent = fmtNumber(getVal(mRow, ['Cafes']));
  }

  function highlightMapCategory(category) {
    destinations.forEach(name => {
      const meta = DESTINATION_META[name];
      const marker = mapMarkers[name];
      if (!marker || !meta) return;

      const el = marker.getElement();
      if (!el) return;

      if (category === 'all' || meta.category === category) {
        el.style.opacity = '1';
        el.style.transform = 'scale(1)';
      } else {
        el.style.opacity = '0.35';
        el.style.transform = 'scale(0.85)';
      }
    });
  }

  // 7. Destination Quick List Carousel
  function renderDestQuickList(filterCategory = 'all') {
    const container = document.getElementById('destQuickList');
    if (!container) return;

    container.innerHTML = '';

    destinations.forEach(name => {
      const meta = DESTINATION_META[name] || {};
      if (filterCategory !== 'all' && meta.category !== filterCategory) return;

      const mRow = getMasterRow(name);
      const visits = getVal(mRow, ['Domestic_Visits_2022', 'Domestic_Visits']);
      const stays = getVal(mRow, ['Total_Accommodation_Listings']);

      const item = document.createElement('div');
      item.className = `dest-card-item ${name === currentDestination ? 'active' : ''}`;
      item.dataset.dest = name;

      item.innerHTML = `
        <div class="dest-item-thumb" style="background-image: url('${meta.thumb || ''}')"></div>
        <div class="dest-item-info">
          <div class="dest-item-top">
            <span class="dest-item-name">${name}</span>
            <span class="dest-item-badge ${meta.category || ''}">${meta.district || ''}</span>
          </div>
          <div class="dest-item-sub">
            <span>👥 ${fmtCompact(visits)}</span>
            <span>🏨 ${stays} Stays</span>
            <span>☕ ${getVal(mRow, ['Cafes'])} Cafes</span>
          </div>
        </div>
      `;

      item.addEventListener('click', () => {
        selectDestination(name, false);
      });

      container.appendChild(item);
    });
  }

  // 8. Destination 360° Navigation Bar (Pills)
  function renderDestPills() {
    const container = document.getElementById('destSelectorBar');
    if (!container) return;

    container.innerHTML = '';

    destinations.forEach(name => {
      const meta = DESTINATION_META[name] || {};
      const btn = document.createElement('button');
      btn.className = `dest-tab-btn ${name === currentDestination ? 'active' : ''}`;
      btn.dataset.dest = name;

      const icon = meta.category === 'hill' ? '🏔' : meta.category === 'coastal' ? '🏖' : meta.category === 'backwaters' ? '⛵' : '🏙';

      btn.innerHTML = `<span class="dest-tab-icon">${icon}</span> ${name}`;

      btn.addEventListener('click', () => {
        selectDestination(name, false);
      });

      container.appendChild(btn);
    });
  }

  // 8B. Executive Home Page Interactive Modules
  function initHomeMiniMap() {
    const mapBox = document.getElementById('keralaMiniMap');
    if (!mapBox) return;

    if (typeof L === 'undefined') {
      mapBox.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#64748b;font-size:11px;">Map loading...</div>';
      return;
    }

    try {
      homeMiniMap = L.map('keralaMiniMap', {
        center: [10.35, 76.45],
        zoom: 6.8,
        zoomSnap: 0.1,
        zoomControl: false,
        attributionControl: false,
        scrollWheelZoom: false,
        dragging: true
      });

      // OpenStreetMap tiles for clean, clear geographic coastline without watermark
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap'
      }).addTo(homeMiniMap);

      // Render pins for all 10 destinations
      destinations.forEach(name => {
        const meta = DESTINATION_META[name];
        if (!meta) return;

        const iconHtml = `<div class="mini-map-pin ${name === currentDestination ? 'active' : ''}" data-dest="${name}" title="${name}"></div>`;
        const pinIcon = L.divIcon({
          className: 'custom-mini-leaflet-pin',
          html: iconHtml,
          iconSize: [18, 18],
          iconAnchor: [9, 9]
        });

        const marker = L.marker([meta.lat, meta.lng], { icon: pinIcon }).addTo(homeMiniMap);
        homeMiniMarkers[name] = marker;

        marker.on('click', () => {
          selectDestination(name, false);
        });
      });
    } catch (err) {
      console.warn('Mini Leaflet Map initialization warning:', err);
    }
  }

  function updateHomeMiniMap(destName) {
    if (!homeMiniMap) return;
    const meta = DESTINATION_META[destName];
    if (meta) {
      homeMiniMap.panTo([meta.lat, meta.lng], { animate: true, duration: 0.4 });
    }
    // Update pin classes
    destinations.forEach(name => {
      const marker = homeMiniMarkers[name];
      if (marker) {
        const el = marker.getElement();
        if (el) {
          const pinEl = el.querySelector('.mini-map-pin');
          if (pinEl) {
            pinEl.classList.toggle('active', name === destName);
          }
        }
      }
    });
  }

  let activeMapCategory = 'all';

  function renderHomeDestPills() {
    const container = document.getElementById('homeDestPills');
    if (!container) return;

    container.innerHTML = '';
    const filteredList = activeMapCategory === 'all'
      ? destinations
      : destinations.filter(d => DESTINATION_META[d] && DESTINATION_META[d].category === activeMapCategory);

    filteredList.forEach(name => {
      const btn = document.createElement('button');
      btn.className = `dest-pill-btn ${name === currentDestination ? 'active' : ''}`;
      btn.textContent = name;
      btn.dataset.dest = name;

      btn.addEventListener('click', () => {
        selectDestination(name, false);
      });

      container.appendChild(btn);
    });

    // Auto-scroll active destination pill into view if needed
    const activeBtn = container.querySelector('.dest-pill-btn.active');
    if (activeBtn) {
      activeBtn.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  function renderHomeTrendChart(destName) {
    const canvas = document.getElementById('homeTrendChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const titleEl = document.getElementById('homeTrendTitle');
    if (titleEl) titleEl.textContent = destName;

    const rows = getSeasonalRows(destName);
    const mRow = getMasterRow(destName);
    const v22 = getVal(mRow, ['Domestic_Visits_2022', 'Domestic_Visits'], 500000);
    const v25 = getVal(mRow, ['Domestic_Visits_2025'], v22 * 1.15);

    let labels = [];
    let dataPoints = [];

    if (homeTrendMode === 'seasonality') {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      labels = months;
      dataPoints = months.map((m, idx) => {
        const found = rows.find(r => Number(r.Month || r.month) === idx + 1);
        if (found) {
          const rawIdx = Number(found.Seasonal_Index || 100);
          return Math.min(100, Math.max(10, Math.round(rawIdx * 0.75)));
        }
        return 50;
      });
    } else {
      // Last 3 Years (2023, 2024, 2025 quarterly sequence)
      labels = [
        '2023 Q1', '2023 Q2', '2023 Q3', '2023 Q4',
        '2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4',
        '2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4'
      ];

      // Growth multiplier from 2022 to 2025
      const growthRatio = v22 > 0 ? (v25 / v22) : 1.2;
      const baseScore = Math.min(65, Math.max(35, Math.round((v22 / 3000000) * 40 + 35)));

      // Extract quarterly seasonal factors from destination's rows
      const getQFactor = (qNum) => {
        const startM = (qNum - 1) * 3 + 1;
        const qRows = rows.filter(r => {
          const m = Number(r.Month || r.month);
          return m >= startM && m < startM + 3;
        });
        if (qRows.length === 0) return 1.0;
        const avg = qRows.reduce((acc, r) => acc + Number(r.Seasonal_Index || 100), 0) / qRows.length;
        return avg / 100.0;
      };

      const qFactors = [getQFactor(1), getQFactor(2), getQFactor(3), getQFactor(4)];

      dataPoints = labels.map((lbl, idx) => {
        const yearIdx = Math.floor(idx / 4);
        const qIdx = idx % 4;
        const yearProgress = (yearIdx + qIdx * 0.25) / 2.75;
        const trendMultiplier = 1.0 + (growthRatio - 1.0) * yearProgress;
        const seasonalMod = qFactors[qIdx];
        
        let val = Math.round(baseScore * trendMultiplier * seasonalMod);
        return Math.min(96, Math.max(18, val));
      });
    }

    if (chartHomeTrend) {
      chartHomeTrend.destroy();
    }

    // Emerald gradient fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 220);
    gradient.addColorStop(0, 'rgba(5, 150, 105, 0.22)');
    gradient.addColorStop(1, 'rgba(5, 150, 105, 0.01)');

    chartHomeTrend = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Tourism Demand',
          data: dataPoints,
          borderColor: '#059669',
          backgroundColor: gradient,
          fill: true,
          tension: 0.42,
          pointRadius: 4.5,
          pointHoverRadius: 7,
          pointBackgroundColor: '#10b981',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          borderWidth: 2.8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            titleFont: { family: 'Outfit', size: 12 },
            bodyFont: { family: 'Plus Jakarta Sans', size: 12 },
            padding: 10,
            cornerRadius: 8,
            callbacks: {
              label: (item) => ` Tourism Index: ${item.parsed.y}/100`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#94a3b8',
              font: { family: 'Plus Jakarta Sans', size: 11 }
            }
          },
          y: {
            min: 0,
            max: 100,
            ticks: {
              stepSize: 25,
              color: '#94a3b8',
              font: { family: 'Plus Jakarta Sans', size: 11 }
            },
            grid: {
              color: 'rgba(226, 232, 240, 0.6)'
            }
          }
        }
      }
    });
  }

  function renderHomeSpotlight(destName) {
    const meta = DESTINATION_META[destName] || {};
    const cRow = getClusterRow(destName);
    const opp = OPPORTUNITY_DATA[destName] || {
      score: 80,
      checks: ['Strong Tourist Interest', 'Growing Visitor Count', 'Good Business Scope'],
      opportunities: [],
      insights: []
    };

    const banner = document.getElementById('homeSpotlightBanner');
    const nameEl = document.getElementById('homeSpotlightName');
    const distEl = document.getElementById('homeSpotlightDistrict');
    const clusterEl = document.getElementById('homeSpotlightCluster');
    const scoreText = document.getElementById('homeScoreText');
    const scoreCircle = document.getElementById('homeScoreCircle');

    if (banner && meta.photo) {
      banner.style.backgroundImage = `url('${meta.photo}')`;
    }

    if (nameEl) {
      nameEl.textContent = destName;
    }
    if (distEl) {
      distEl.textContent = `${meta.district} District • ${meta.keralaTag || ''}`;
    }

    const clusterId = cRow.Cluster !== undefined ? Number(cRow.Cluster) : 0;
    if (clusterEl) {
      clusterEl.textContent = clusterId === 1 ? 'Cluster 1 • High Demand' : 'Cluster 0 • Nature & Leisure';
    }

    // Circular Progress Gauge (circumference: 2 * Math.PI * 38 ≈ 238.76)
    if (scoreText) scoreText.textContent = `${opp.score}%`;
    if (scoreCircle) {
      const circumference = 238.76;
      const offset = circumference * (1 - (opp.score / 100));
      scoreCircle.style.strokeDashoffset = offset.toFixed(1);
    }

    // Checkmarks
    const c1 = document.getElementById('scoreCheck1');
    const c2 = document.getElementById('scoreCheck2');
    const c3 = document.getElementById('scoreCheck3');
    if (c1 && opp.checks[0]) c1.textContent = opp.checks[0];
    if (c2 && opp.checks[1]) c2.textContent = opp.checks[1];
    if (c3 && opp.checks[2]) c3.textContent = opp.checks[2];
  }

  function renderHomeLandscapeDonut(destName) {
    const canvas = document.getElementById('homeLandscapeChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const titleEl = document.getElementById('homeLandscapeTitle');
    if (titleEl) titleEl.textContent = destName;

    const mRow = getMasterRow(destName);
    const hotels = getVal(mRow, ['Hotels']);
    const resorts = getVal(mRow, ['Resorts']);
    const rests = getVal(mRow, ['Restaurants']);
    const cafes = getVal(mRow, ['Cafes']);
    const homestays = getVal(mRow, ['Homestays']);
    const villas = getVal(mRow, ['Serviced_Villas', 'ServicedVillas']);
    const boats = getVal(mRow, ['Houseboats']);
    const others = villas + boats;

    const totalStays = hotels + resorts;
    const totalAll = Math.max(1, totalStays + rests + cafes + homestays + others);

    const pctHotels = Math.max(1, Math.round((totalStays / totalAll) * 100));
    const pctRests = Math.max(1, Math.round((rests / totalAll) * 100));
    const pctCafes = Math.max(1, Math.round((cafes / totalAll) * 100));
    const pctHome = Math.max(1, Math.round((homestays / totalAll) * 100));
    const pctOthers = Math.max(0, 100 - (pctHotels + pctRests + pctCafes + pctHome));

    // Update legend numbers
    const lHotels = document.getElementById('legHotelsPct');
    const lRest = document.getElementById('legRestPct');
    const lCafes = document.getElementById('legCafesPct');
    const lHome = document.getElementById('legHomePct');
    const lOthers = document.getElementById('legOthersPct');
    const lTotal = document.getElementById('homeLandscapeTotal');

    if (lHotels) lHotels.textContent = `${pctHotels}%`;
    if (lRest) lRest.textContent = `${pctRests}%`;
    if (lCafes) lCafes.textContent = `${pctCafes}%`;
    if (lHome) lHome.textContent = `${pctHome}%`;
    if (lOthers) lOthers.textContent = `${pctOthers}%`;
    if (lTotal) {
      lTotal.textContent = totalAll >= 1000 ? `${(totalAll / 1000).toFixed(1)}K` : String(totalAll);
    }

    if (chartHomeLandscape) {
      chartHomeLandscape.destroy();
    }

    chartHomeLandscape = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Hotels & Resorts', 'Restaurants', 'Cafes', 'Homestays', 'Others'],
        datasets: [{
          data: [pctHotels, pctRests, pctCafes, pctHome, pctOthers],
          backgroundColor: ['#3b82f6', '#f97316', '#10b981', '#a855f7', '#94a3b8'],
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            callbacks: {
              label: (item) => ` ${item.label}: ${item.parsed}%`
            }
          }
        }
      }
    });
  }

  function renderHomeOpportunities(destName) {
    const opp = OPPORTUNITY_DATA[destName] || OPPORTUNITY_DATA.Munnar;
    if (!opp || !opp.opportunities) return;

    const list = opp.opportunities;
    if (list[0]) {
      const img = document.getElementById('homeOpp1Img');
      const t = document.getElementById('homeOpp1Title');
      const d = document.getElementById('homeOpp1Desc');
      const b = document.getElementById('homeOpp1Badge');
      if (img && list[0].img) img.src = list[0].img;
      if (t) t.textContent = list[0].title;
      if (d) d.textContent = list[0].desc;
      if (b) {
        b.textContent = list[0].tag;
        b.className = `opp-tag ${list[0].tag.toLowerCase() === 'high' ? 'green' : 'orange'}`;
      }
    }
    if (list[1]) {
      const img = document.getElementById('homeOpp2Img');
      const t = document.getElementById('homeOpp2Title');
      const d = document.getElementById('homeOpp2Desc');
      const b = document.getElementById('homeOpp2Badge');
      if (img && list[1].img) img.src = list[1].img;
      if (t) t.textContent = list[1].title;
      if (d) d.textContent = list[1].desc;
      if (b) {
        b.textContent = list[1].tag;
        b.className = `opp-tag ${list[1].tag.toLowerCase() === 'high' ? 'green' : 'orange'}`;
      }
    }
    if (list[2]) {
      const img = document.getElementById('homeOpp3Img');
      const t = document.getElementById('homeOpp3Title');
      const d = document.getElementById('homeOpp3Desc');
      const b = document.getElementById('homeOpp3Badge');
      if (img && list[2].img) img.src = list[2].img;
      if (t) t.textContent = list[2].title;
      if (d) d.textContent = list[2].desc;
      if (b) {
        b.textContent = list[2].tag;
        b.className = `opp-tag ${list[2].tag.toLowerCase() === 'high' ? 'green' : 'orange'}`;
      }
    }
  }

  function renderHomeQuickInsights(destName) {
    const opp = OPPORTUNITY_DATA[destName] || OPPORTUNITY_DATA.Munnar;
    if (!opp || !opp.insights) return;

    const q1 = document.getElementById('homeQi1');
    const q2 = document.getElementById('homeQi2');
    const q3 = document.getElementById('homeQi3');
    if (q1 && opp.insights[0]) q1.textContent = opp.insights[0];
    if (q2 && opp.insights[1]) q2.textContent = opp.insights[1];
    if (q3 && opp.insights[2]) q3.textContent = opp.insights[2];
  }

  // 9. Core Destination Selection Handler (Synchronizes Entire App)
  function selectDestination(destName, navigateToDeepDive = false) {
    if (!destinations.includes(destName)) return;
    currentDestination = destName;

    // Update Quick List Active states
    document.querySelectorAll('.dest-card-item').forEach(el => {
      el.classList.toggle('active', el.dataset.dest === destName);
    });

    // Update Pills Active states
    document.querySelectorAll('.dest-tab-btn').forEach(el => {
      el.classList.toggle('active', el.dataset.dest === destName);
    });

    // Update Home Page Components
    updateHomeMiniMap(destName);
    renderHomeDestPills();
    renderHomeTrendChart(destName);
    renderHomeSpotlight(destName);
    renderHomeLandscapeDonut(destName);
    renderHomeOpportunities(destName);
    renderHomeQuickInsights(destName);

    // Update Deep Dive Overview Map if present
    updateMapOverlay(destName);
    if (mapMarkers[destName] && leafletMap) {
      const meta = DESTINATION_META[destName];
      if (meta) {
        leafletMap.panTo([meta.lat, meta.lng], { animate: true, duration: 0.5 });
      }
    }

    // Render Deep Dive View
    renderDestinationHero(destName);
    renderSeasonalityChart(destName);
    renderAccommodationDonut(destName);
    renderFoodAndBeverageMetrics(destName);
    renderStrategicInsights(destName);

    // If navigation requested
    if (navigateToDeepDive) {
      window.location.hash = '#destinations';
      const destNav = document.querySelector('.nav-link[data-nav="destinations"]');
      if (destNav) destNav.click();
    }
  }

  // Expose global callback for map popup and cultural modal links
  window.selectKeralaDest = function (name, navigate = false) {
    const modal = document.getElementById('keralaHeritageModal');
    if (modal) modal.style.display = 'none';
    selectDestination(name, navigate);
  };

  // 10. Destination Hero Card
  function renderDestinationHero(destName) {
    const meta = DESTINATION_META[destName] || {};
    const mRow = getMasterRow(destName);
    const cRow = getClusterRow(destName);

    const heroBg = document.getElementById('destHeroBg');
    const title = document.getElementById('heroDestTitle');
    const desc = document.getElementById('heroDestDesc');
    const districtBadge = document.getElementById('heroDistrictBadge');
    const categoryBadge = document.getElementById('heroCategoryBadge');
    const clusterBadge = document.getElementById('heroClusterBadge');

    const visits2022 = document.getElementById('heroVisits2022');
    const visits2025 = document.getElementById('heroVisits2025');
    const growthBadge = document.getElementById('heroGrowthBadge');
    const foreignVisits = document.getElementById('heroForeignVisits');
    const trendsScore = document.getElementById('heroTrendsScore');

    if (heroBg && meta.photo) {
      heroBg.style.backgroundImage = `url('${meta.photo}')`;
    }

    if (title) {
      title.textContent = destName;
    }
    if (desc) desc.textContent = meta.desc || '';
    if (districtBadge) districtBadge.textContent = `${meta.district} District • ${meta.keralaTag || ''}`;
    if (categoryBadge) categoryBadge.textContent = meta.categoryLabel || '';

    const clusterId = cRow.Cluster !== undefined ? Number(cRow.Cluster) : 0;
    if (clusterBadge) {
      clusterBadge.textContent = clusterId === 1 ? 'Cluster 1: Urban Gateway Market' : 'Cluster 0: Nature & Leisure Haven';
      clusterBadge.style.display = 'inline-block';
    }

    const v22 = getVal(mRow, ['Domestic_Visits_2022', 'Domestic_Visits']);
    const v25 = getVal(mRow, ['Domestic_Visits_2025']);
    const fVisits = getVal(mRow, ['Foreign_Visits_2025', 'Foreign_Visits_2022']);
    const tScore = getVal(mRow, ['Google_Trends_Mean_Interest_Descriptive_Only', 'Google_Trends_Last_12_Month_Mean_Descriptive_Only']);

    if (visits2022) visits2022.textContent = fmtNumber(v22);

    if (visits2025) {
      visits2025.textContent = v25 ? fmtNumber(v25) : '—';
    }

    if (growthBadge) {
      if (v22 > 0 && v25 > 0) {
        const growth = Math.round(((v25 - v22) / v22) * 100);
        growthBadge.style.display = 'inline-block';
        growthBadge.textContent = `${growth >= 0 ? '+' : ''}${growth}%`;
        growthBadge.className = `hm-badge ${growth >= 0 ? 'up' : 'down'}`;
      } else {
        growthBadge.style.display = 'none';
      }
    }

    if (foreignVisits) {
      foreignVisits.textContent = fVisits ? fmtNumber(fVisits) : 'N/A';
    }

    if (trendsScore) {
      trendsScore.textContent = tScore ? Number(tScore).toFixed(1) : '—';
    }
  }

  // 11. Seasonality & Google Trends Chart (Chart.js)
  function renderSeasonalityChart(destName) {
    const ctx = document.getElementById('seasonalityChart');
    if (!ctx) return;

    const rows = getSeasonalRows(destName);
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    // Map month 1-12 to values
    const dataVals = months.map((mName, idx) => {
      const monthNum = idx + 1;
      const found = rows.find(r => Number(r.Month || r.month) === monthNum);
      if (!found) return 0;
      return activeSeasonalityMode === 'index'
        ? getVal(found, ['Seasonal_Index', 'SeasonalIndex', 'Index'], 100)
        : getVal(found, ['interest', 'Interest', 'Trend_Score'], 0);
    });

    // Compute min / max / spread
    let maxIdx = 0, minIdx = 0;
    dataVals.forEach((val, i) => {
      if (val > dataVals[maxIdx]) maxIdx = i;
      if (val < dataVals[minIdx]) minIdx = i;
    });

    const peakMonth = months[maxIdx];
    const lowMonth = months[minIdx];
    const peakVal = dataVals[maxIdx];
    const lowVal = dataVals[minIdx];
    const spread = lowVal > 0 ? (peakVal / lowVal).toFixed(2) + 'x' : '—';

    const pEl = document.getElementById('seasonPeakMonth');
    const pValEl = document.getElementById('seasonPeakVal');
    const lEl = document.getElementById('seasonLowMonth');
    const lValEl = document.getElementById('seasonLowVal');
    const sEl = document.getElementById('seasonSpread');

    if (pEl) pEl.textContent = peakMonth;
    if (pValEl) pValEl.textContent = activeSeasonalityMode === 'index' ? `${peakVal.toFixed(1)}%` : peakVal.toFixed(1);
    if (lEl) lEl.textContent = lowMonth;
    if (lValEl) lValEl.textContent = activeSeasonalityMode === 'index' ? `${lowVal.toFixed(1)}%` : lowVal.toFixed(1);
    if (sEl) sEl.textContent = spread;

    if (chartSeasonality) {
      chartSeasonality.destroy();
    }

    if (typeof Chart === 'undefined') return;

    const isIndex = activeSeasonalityMode === 'index';

    chartSeasonality = new Chart(ctx, {
      type: 'line',
      data: {
        labels: months,
        datasets: [{
          label: isIndex ? 'Seasonal Index (%)' : 'Google Trends Relative Interest',
          data: dataVals,
          borderColor: '#059669',
          backgroundColor: 'rgba(5, 150, 105, 0.12)',
          fill: true,
          tension: 0.38,
          pointBackgroundColor: '#059669',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          borderWidth: 2.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            titleFont: { size: 12, family: 'Plus Jakarta Sans' },
            bodyFont: { size: 12, family: 'Plus Jakarta Sans' },
            padding: 10,
            cornerRadius: 8,
            callbacks: {
              label: function (context) {
                return isIndex ? ` Seasonal Index: ${context.parsed.y.toFixed(1)}%` : ` Interest Score: ${context.parsed.y.toFixed(1)}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: '#64748b', font: { size: 11 } }
          },
          y: {
            grid: { color: 'rgba(226, 232, 240, 0.7)' },
            ticks: {
              color: '#64748b',
              font: { size: 11 },
              callback: function (value) {
                return isIndex ? `${value}%` : value;
              }
            }
          }
        }
      }
    });

    // Toggle Buttons Handler
    const btnIndex = document.getElementById('btnToggleSeasonality');
    const btnTrends = document.getElementById('btnToggleTrends');

    if (btnIndex && btnTrends) {
      btnIndex.onclick = () => {
        activeSeasonalityMode = 'index';
        btnIndex.classList.add('active');
        btnTrends.classList.remove('active');
        renderSeasonalityChart(destName);
      };

      btnTrends.onclick = () => {
        activeSeasonalityMode = 'interest';
        btnTrends.classList.add('active');
        btnIndex.classList.remove('active');
        renderSeasonalityChart(destName);
      };
    }
  }

  // 12. Accommodation Donut Chart & Legend
  function renderAccommodationDonut(destName) {
    const ctx = document.getElementById('accomDonutChart');
    if (!ctx) return;

    const mRow = getMasterRow(destName);
    const hotels = getVal(mRow, ['Hotels']);
    const homestays = getVal(mRow, ['Homestays']);
    const resorts = getVal(mRow, ['Resorts']);
    const villas = getVal(mRow, ['Serviced_Villas', 'Villas']);
    const houseboats = getVal(mRow, ['Houseboats']);

    const total = hotels + homestays + resorts + villas + houseboats;

    const totalPill = document.getElementById('accomTotalPill');
    const centerTotal = document.getElementById('donutCenterTotal');
    if (totalPill) totalPill.textContent = `Total: ${fmtNumber(total)}`;
    if (centerTotal) centerTotal.textContent = fmtNumber(total);

    const categories = [
      { label: 'Hotels', count: hotels, color: '#0284c7' },
      { label: 'Homestays', count: homestays, color: '#10b981' },
      { label: 'Resorts', count: resorts, color: '#f59e0b' },
      { label: 'Serviced Villas', count: villas, color: '#8b5cf6' },
      { label: 'Houseboats', count: houseboats, color: '#0d9488' }
    ];

    // Render HTML Legend Grid
    const legendGrid = document.getElementById('accomLegendGrid');
    if (legendGrid) {
      legendGrid.innerHTML = '';
      categories.forEach(cat => {
        const pct = total > 0 ? Math.round((cat.count / total) * 100) : 0;
        const row = document.createElement('div');
        row.className = 'legend-row';
        row.innerHTML = `
          <div class="legend-left">
            <span class="legend-color-dot" style="background:${cat.color}"></span>
            <span>${cat.label}</span>
          </div>
          <span class="legend-val">${cat.count} (${pct}%)</span>
        `;
        legendGrid.appendChild(row);
      });
    }

    if (chartAccomDonut) {
      chartAccomDonut.destroy();
    }

    if (typeof Chart === 'undefined') return;

    chartAccomDonut = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categories.map(c => c.label),
        datasets: [{
          data: categories.map(c => c.count),
          backgroundColor: categories.map(c => c.color),
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            padding: 10,
            cornerRadius: 8,
            callbacks: {
              label: function (context) {
                const val = context.raw || 0;
                const pct = total > 0 ? Math.round((val / total) * 100) : 0;
                return ` ${context.label}: ${val} listings (${pct}%)`;
              }
            }
          }
        }
      }
    });
  }

  // 13. Food & Beverage Density & Pressure
  function renderFoodAndBeverageMetrics(destName) {
    const mRow = getMasterRow(destName);
    const oppRow = getOpportunityRow(destName);

    const restaurants = getVal(mRow, ['Restaurants']);
    const cafes = getVal(mRow, ['Cafes']);

    const restEl = document.getElementById('fbRestaurants');
    const cafeEl = document.getElementById('fbCafes');
    if (restEl) restEl.textContent = fmtNumber(restaurants);
    if (cafeEl) cafeEl.textContent = fmtNumber(cafes);

    const vPerCafe = getVal(oppRow, ['Visits_Per_Cafe']);
    const vPerRest = getVal(oppRow, ['Visits_Per_Restaurant']);
    const cafeRank = getVal(oppRow, ['Cafe_Rank'], 10);
    const restRank = getVal(oppRow, ['Restaurant_Rank'], 10);

    const vpcEl = document.getElementById('visitsPerCafeVal');
    const vprEl = document.getElementById('visitsPerRestVal');
    const crbEl = document.getElementById('cafeRankBadge');
    const rrbEl = document.getElementById('restRankBadge');
    const cafeBar = document.getElementById('cafeBarFill');
    const restBar = document.getElementById('restBarFill');
    const cafeNote = document.getElementById('cafeGaugeNote');
    const restNote = document.getElementById('restGaugeNote');

    if (vpcEl) vpcEl.textContent = vPerCafe ? fmtNumber(Math.round(vPerCafe)) : '—';
    if (vprEl) vprEl.textContent = vPerRest ? fmtNumber(Math.round(vPerRest)) : '—';

    function getRankClass(rank) {
      if (rank <= 3) return 'rank-tag gold';
      if (rank <= 7) return 'rank-tag silver';
      return 'rank-tag bronze';
    }

    if (crbEl) {
      crbEl.className = getRankClass(cafeRank);
      crbEl.textContent = `Rank #${cafeRank}`;
    }

    if (rrbEl) {
      rrbEl.className = getRankClass(restRank);
      rrbEl.textContent = `Rank #${restRank}`;
    }

    // Relative progress percentage (Munnar max ~28,217)
    if (cafeBar) {
      const pct = Math.min(100, Math.max(15, Math.round((vPerCafe / 28217) * 100)));
      cafeBar.style.width = `${pct}%`;
    }

    if (restBar) {
      const pct = Math.min(100, Math.max(15, Math.round((vPerRest / 5828) * 100)));
      restBar.style.width = `${pct}%`;
    }

    if (cafeNote) {
      if (cafeRank <= 3) {
        cafeNote.textContent = 'High Deficit: Severe scarcity of specialty cafes relative to tourist inflow';
      } else if (cafeRank <= 7) {
        cafeNote.textContent = 'Moderate Supply: Balanced cafe density with selective niche room';
      } else {
        cafeNote.textContent = 'Well Supplied: High cafe density per visitor (e.g., cliff beach or metro)';
      }
    }

    if (restNote) {
      if (restRank <= 3) {
        restNote.textContent = 'Elevated Dining Load: Heavy pressure during holiday meal rushes';
      } else {
        restNote.textContent = 'Established Dining Footprint: Broad commercial culinary network';
      }
    }
  }

  // 14. Dynamic Strategic Insights Generator
  function renderStrategicInsights(destName) {
    const container = document.getElementById('insightsGrid');
    if (!container) return;

    const mRow = getMasterRow(destName);
    const oppRow = getOpportunityRow(destName);
    const cRow = getClusterRow(destName);

    const visits = getVal(mRow, ['Domestic_Visits_2022', 'Domestic_Visits']);
    const hotels = getVal(mRow, ['Hotels']);
    const homestays = getVal(mRow, ['Homestays']);
    const cafes = getVal(mRow, ['Cafes']);
    const cafeRank = getVal(oppRow, ['Cafe_Rank'], 5);
    const clusterId = Number(cRow.Cluster || 0);

    const insights = [
      {
        icon: '📊',
        title: 'Visitor Density & Market Scale',
        desc: `${destName} registers ${fmtNumber(visits)} recorded domestic visits, positioning it within ${clusterId === 1 ? 'the urban economic core' : 'the leisure tourism corridor'} of Kerala.`
      },
      {
        icon: '☕',
        title: 'F&B Investment Screening',
        desc: cafeRank <= 3
          ? `Ranks #${cafeRank} in cafe deficit statewide. With only ${cafes} recorded cafes, high tourist volume creates a prime window for specialty coffee and bakeries.`
          : `Rank #${cafeRank} in cafe pressure. Benefits from ${cafes} established cafes, suggesting boutique differentiation is key for new entrants.`
      },
      {
        icon: '🏡',
        title: 'Accommodation Architecture',
        desc: homestays > hotels
          ? `Experiential lodging dominates: homestays (${homestays}) outnumber traditional hotels (${hotels}), highlighting high appetite for community tourism.`
          : `Traditional lodging leads with ${hotels} hotels and ${homestays} homestays. Scope exists for experiential villas and boutique eco-retreats.`
      },
      {
        icon: '📈',
        title: 'Seasonality & Operational Rhythm',
        desc: `High holiday peaks in winter months contrast with monsoon troughs in June–July. Operators should pair monsoon discounts with experiential wellness packages.`
      }
    ];

    container.innerHTML = '';
    insights.forEach(item => {
      const card = document.createElement('div');
      card.className = 'insight-item';
      card.innerHTML = `
        <div class="insight-icon">${item.icon}</div>
        <div class="insight-text">
          <h5>${item.title}</h5>
          <p>${item.desc}</p>
        </div>
      `;
      container.appendChild(card);
    });
  }

  // 15. Opportunity Screening Full Table & Sorting
  function renderOpportunityTable() {
    const tbody = document.getElementById('opportunityTableBody');
    if (!tbody) return;

    // Merge opportunities with master data for display
    let dataset = destinations.map(dest => {
      const opp = getOpportunityRow(dest);
      const m = getMasterRow(dest);
      return {
        Destination: dest,
        Domestic_Visits_2022: getVal(opp, ['Domestic_Visits_2022']) || getVal(m, ['Domestic_Visits_2022']),
        Total_Accommodation_Listings: getVal(opp, ['Total_Accommodation_Listings']) || getVal(m, ['Total_Accommodation_Listings']),
        Visits_Per_Accommodation: getVal(opp, ['Visits_Per_Accommodation']),
        Accommodation_Rank: getVal(opp, ['Accommodation_Rank'], 99),
        Restaurants: getVal(opp, ['Restaurants']) || getVal(m, ['Restaurants']),
        Visits_Per_Restaurant: getVal(opp, ['Visits_Per_Restaurant']),
        Restaurant_Rank: getVal(opp, ['Restaurant_Rank'], 99),
        Cafes: getVal(opp, ['Cafes']) || getVal(m, ['Cafes']),
        Visits_Per_Cafe: getVal(opp, ['Visits_Per_Cafe']),
        Cafe_Rank: getVal(opp, ['Cafe_Rank'], 99)
      };
    });

    // Apply Filter if search active
    const searchVal = (document.getElementById('oppTableSearch')?.value || '').toLowerCase();
    if (searchVal) {
      dataset = dataset.filter(row => row.Destination.toLowerCase().includes(searchVal));
    }

    // Apply Sorting
    dataset.sort((a, b) => {
      let valA = a[currentSort.column];
      let valB = b[currentSort.column];
      if (typeof valA === 'string') {
        return currentSort.order === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }
      return currentSort.order === 'asc' ? valA - valB : valB - valA;
    });

    tbody.innerHTML = '';

    dataset.forEach(row => {
      const tr = document.createElement('tr');
      if (row.Destination === currentDestination) {
        tr.style.backgroundColor = 'rgba(5, 150, 105, 0.08)';
      }

      function rankTag(rank) {
        if (rank <= 3) return `<span class="rank-tag gold">#${rank}</span>`;
        if (rank <= 7) return `<span class="rank-tag silver">#${rank}</span>`;
        return `<span class="rank-tag bronze">#${rank}</span>`;
      }

      tr.innerHTML = `
        <td><strong>${row.Destination}</strong></td>
        <td>${fmtNumber(row.Domestic_Visits_2022)}</td>
        <td>${row.Total_Accommodation_Listings}</td>
        <td><b>${fmtNumber(Math.round(row.Visits_Per_Accommodation))}</b></td>
        <td>${rankTag(row.Accommodation_Rank)}</td>
        <td>${row.Restaurants}</td>
        <td>${fmtNumber(Math.round(row.Visits_Per_Restaurant))}</td>
        <td>${row.Cafes}</td>
        <td><b style="color:#059669">${fmtNumber(Math.round(row.Visits_Per_Cafe))}</b></td>
        <td>${rankTag(row.Cafe_Rank)}</td>
        <td>
          <button class="btn btn-secondary btn-xs" onclick="window.selectKeralaDest('${row.Destination}', true)">
            Inspect →
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    // Bind Sorting Headers
    document.querySelectorAll('#opportunityTable th[data-sort]').forEach(th => {
      th.onclick = () => {
        const col = th.dataset.sort;
        if (currentSort.column === col) {
          currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
        } else {
          currentSort.column = col;
          currentSort.order = 'desc';
        }
        renderOpportunityTable();
      };
    });

    const searchInput = document.getElementById('oppTableSearch');
    if (searchInput) {
      searchInput.oninput = () => renderOpportunityTable();
    }
  }

  // 16. Head-to-Head Destination Comparator
  function initComparator() {
    const selectA = document.getElementById('compareSelectA');
    const selectB = document.getElementById('compareSelectB');

    if (!selectA || !selectB) return;

    function refreshComparison() {
      const destA = selectA.value;
      const destB = selectB.value;

      renderComparatorTable(destA, destB);
      renderComparatorBarChart(destA, destB);
      renderComparatorSeasonChart(destA, destB);
    }

    selectA.addEventListener('change', refreshComparison);
    selectB.addEventListener('change', refreshComparison);

    refreshComparison();
  }

  function renderComparatorTable(destA, destB) {
    const tbody = document.getElementById('compareTableBody');
    const colHeadA = document.getElementById('compareColHeadA');
    const colHeadB = document.getElementById('compareColHeadB');

    if (colHeadA) colHeadA.textContent = destA;
    if (colHeadB) colHeadB.textContent = destB;
    if (!tbody) return;

    const rowA = getMasterRow(destA);
    const rowB = getMasterRow(destB);
    const oppA = getOpportunityRow(destA);
    const oppB = getOpportunityRow(destB);

    const metrics = [
      {
        label: 'Domestic Footfall (2022)',
        valA: getVal(rowA, ['Domestic_Visits_2022', 'Domestic_Visits']),
        valB: getVal(rowB, ['Domestic_Visits_2022', 'Domestic_Visits']),
        format: fmtNumber
      },
      {
        label: 'Total Accommodation Listings',
        valA: getVal(rowA, ['Total_Accommodation_Listings']),
        valB: getVal(rowB, ['Total_Accommodation_Listings']),
        format: fmtNumber
      },
      {
        label: 'Hotels & Resorts',
        valA: getVal(rowA, ['Hotels']) + getVal(rowA, ['Resorts']),
        valB: getVal(rowB, ['Hotels']) + getVal(rowB, ['Resorts']),
        format: fmtNumber
      },
      {
        label: 'Homestays',
        valA: getVal(rowA, ['Homestays']),
        valB: getVal(rowB, ['Homestays']),
        format: fmtNumber
      },
      {
        label: 'Restaurants Recorded',
        valA: getVal(rowA, ['Restaurants']),
        valB: getVal(rowB, ['Restaurants']),
        format: fmtNumber
      },
      {
        label: 'Specialty Cafes Recorded',
        valA: getVal(rowA, ['Cafes']),
        valB: getVal(rowB, ['Cafes']),
        format: fmtNumber
      },
      {
        label: 'Visits per Recorded Cafe',
        valA: getVal(oppA, ['Visits_Per_Cafe']),
        valB: getVal(oppB, ['Visits_Per_Cafe']),
        format: (n) => fmtNumber(Math.round(n))
      },
      {
        label: 'Cafe Opportunity Rank',
        valA: getVal(oppA, ['Cafe_Rank']),
        valB: getVal(oppB, ['Cafe_Rank']),
        format: (n) => `#${n}`
      }
    ];

    tbody.innerHTML = '';

    metrics.forEach(m => {
      const tr = document.createElement('tr');
      let deltaBadge = '';

      if (typeof m.valA === 'number' && typeof m.valB === 'number' && m.valB > 0 && !m.label.includes('Rank')) {
        const diff = Math.round(((m.valA - m.valB) / m.valB) * 100);
        const isPos = diff >= 0;
        deltaBadge = `<span class="delta-badge ${isPos ? 'positive' : 'negative'}">${isPos ? '+' : ''}${diff}%</span>`;
      } else {
        deltaBadge = `<span class="delta-badge neutral">—</span>`;
      }

      tr.innerHTML = `
        <td><strong>${m.label}</strong></td>
        <td><b>${m.format(m.valA)}</b></td>
        <td>${deltaBadge}</td>
        <td><b>${m.format(m.valB)}</b></td>
      `;

      tbody.appendChild(tr);
    });
  }

  function renderComparatorBarChart(destA, destB) {
    const ctx = document.getElementById('compareBarChart');
    if (!ctx) return;

    const rowA = getMasterRow(destA);
    const rowB = getMasterRow(destB);

    const labels = ['Hotels', 'Resorts', 'Homestays', 'Restaurants', 'Cafes'];
    const dataA = [
      getVal(rowA, ['Hotels']),
      getVal(rowA, ['Resorts']),
      getVal(rowA, ['Homestays']),
      getVal(rowA, ['Restaurants']),
      getVal(rowA, ['Cafes'])
    ];
    const dataB = [
      getVal(rowB, ['Hotels']),
      getVal(rowB, ['Resorts']),
      getVal(rowB, ['Homestays']),
      getVal(rowB, ['Restaurants']),
      getVal(rowB, ['Cafes'])
    ];

    if (chartCompareBar) chartCompareBar.destroy();
    if (typeof Chart === 'undefined') return;

    chartCompareBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: destA,
            data: dataA,
            backgroundColor: '#059669',
            borderRadius: 4
          },
          {
            label: destB,
            data: dataB,
            backgroundColor: '#0284c7',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { font: { family: 'Plus Jakarta Sans', size: 12 } }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: { beginAtZero: true }
        }
      }
    });
  }

  function renderComparatorSeasonChart(destA, destB) {
    const ctx = document.getElementById('compareSeasonChart');
    if (!ctx) return;

    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const rowsA = getSeasonalRows(destA);
    const rowsB = getSeasonalRows(destB);

    function getCurve(rows) {
      return months.map((m, idx) => {
        const found = rows.find(r => Number(r.Month || r.month) === idx + 1);
        return found ? getVal(found, ['Seasonal_Index', 'SeasonalIndex', 'Index'], 100) : 100;
      });
    }

    if (chartCompareSeason) chartCompareSeason.destroy();
    if (typeof Chart === 'undefined') return;

    chartCompareSeason = new Chart(ctx, {
      type: 'line',
      data: {
        labels: months,
        datasets: [
          {
            label: `${destA} Seasonality (%)`,
            data: getCurve(rowsA),
            borderColor: '#059669',
            backgroundColor: 'rgba(5, 150, 105, 0.1)',
            tension: 0.35,
            borderWidth: 2.5
          },
          {
            label: `${destB} Seasonality (%)`,
            data: getCurve(rowsB),
            borderColor: '#0284c7',
            backgroundColor: 'rgba(2, 132, 199, 0.1)',
            tension: 0.35,
            borderWidth: 2.5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.dataset.label}: ${ctx.parsed.y.toFixed(1)}%`
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            ticks: { callback: (v) => `${v}%` }
          }
        }
      }
    });
  }

  // ==========================================================================
  // Kerala Cultural Elements, Modal, Ticker & Ambient Soundscape Engine
  // ==========================================================================

  const KERALA_TRIVIA = [
    "Alappuzha's Kettuvallam houseboats are handcrafted using traditional Anjili wood and coir ropes without a single iron nail.",
    "Munnar's endemic Neelakurinji flower blooms once every 12 years, transforming the Western Ghats into a sea of violet.",
    "Kozhikode became the first city in India to be designated as a UNESCO 'City of Literature' in 2023.",
    "Kochi's iconic Chinese Fishing Nets (Cheena Vala) date back to 14th-century maritime trade under Kublai Khan.",
    "The Periyar Tiger Reserve in Thekkady is India's premier sanctuary for observing wild elephants from lake boats.",
    "Varkala is the only destination in southern Kerala with dramatic red laterite cliffs overlooking the Arabian Sea.",
    "Wayanad is home to the ancient Edakkal Caves featuring Neolithic rock petroglyphs dating back to 6,000 BCE.",
    "Kovalam pioneered modern coastal wellness and Ayurvedic tourism in India, anchored by its iconic 1930s striped lighthouse.",
    "Vagamon's rolling green meadows and pine forests host South India's premier international paragliding championship.",
    "Kumarakom on Vembanad Lake won global UNWTO accolades as a world model for community-driven Responsible Tourism."
  ];

  let currentTickerIdx = 0;
  let tickerTimer = null;

  function initKeralaCulturalTicker() {
    const textEl = document.getElementById('tickerFactText');
    const prevBtn = document.getElementById('tickerPrev');
    const nextBtn = document.getElementById('tickerNext');
    if (!textEl) return;

    function showFact(idx) {
      currentTickerIdx = (idx + KERALA_TRIVIA.length) % KERALA_TRIVIA.length;
      textEl.style.opacity = '0';
      setTimeout(() => {
        textEl.textContent = KERALA_TRIVIA[currentTickerIdx];
        textEl.style.opacity = '1';
      }, 200);
    }

    showFact(0);

    function startTimer() {
      if (tickerTimer) clearInterval(tickerTimer);
      tickerTimer = setInterval(() => {
        showFact(currentTickerIdx + 1);
      }, 7000);
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        showFact(currentTickerIdx + 1);
        startTimer();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        showFact(currentTickerIdx - 1);
        startTimer();
      });
    }

    startTimer();
  }

  function initKeralaHeritageModal() {
    const modal = document.getElementById('keralaHeritageModal');
    const openBtnHeader = document.getElementById('btnOpenHeritageHeader');
    const openBtnSidebar = document.getElementById('btnSidebarHeritage');
    const closeBtn = document.getElementById('btnCloseHeritageModal');
    const tabs = document.querySelectorAll('.kmh-tab-btn');
    const panels = document.querySelectorAll('.kmh-tab-panel');

    function openModal() {
      if (modal) modal.style.display = 'flex';
    }

    function closeModal() {
      if (modal) modal.style.display = 'none';
    }

    if (openBtnHeader) openBtnHeader.addEventListener('click', openModal);
    if (openBtnSidebar) openBtnSidebar.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);

    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
      });
    }

    // Esc key to close modal
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
        closeModal();
      }
    });

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        const targetId = `pane-${tab.dataset.tab}`;
        const targetPanel = document.getElementById(targetId);
        if (targetPanel) targetPanel.classList.add('active');
      });
    });
  }

  function initMapFilterTags() {
    const tagBtns = document.querySelectorAll('.map-tag-btn');
    if (!tagBtns.length) return;

    tagBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tagBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeMapCategory = btn.dataset.cat || 'all';

        // Re-render pills filtered
        renderHomeDestPills();

        // Highlight mini-map pins
        destinations.forEach(name => {
          const meta = DESTINATION_META[name];
          const marker = homeMiniMarkers[name];
          if (!marker || !meta) return;
          const el = marker.getElement();
          if (!el) return;

          if (activeMapCategory === 'all' || meta.category === activeMapCategory) {
            el.style.opacity = '1';
            el.style.transform = 'scale(1)';
          } else {
            el.style.opacity = '0.25';
            el.style.transform = 'scale(0.8)';
          }
        });

        // Also highlight leaflet map if present
        highlightMapCategory(activeMapCategory);
      });
    });
  }

  // Kerala Ambient Soundscape Engine (Pure Web Audio API - zero external downloads)
  let audioCtx = null;
  let isAmbientPlaying = false;
  let bellInterval = null;

  function initKeralaAmbientSound() {
    const btn = document.getElementById('btnKeralaAmbient');
    const text = document.getElementById('ambientText');
    const wave = document.getElementById('soundWave');
    if (!btn) return;

    btn.addEventListener('click', () => {
      if (isAmbientPlaying) {
        // Turn OFF
        if (audioCtx) {
          audioCtx.close();
          audioCtx = null;
        }
        if (bellInterval) clearInterval(bellInterval);
        isAmbientPlaying = false;
        btn.classList.remove('active');
        if (text) text.textContent = 'Kerala Ambience: Off';
        if (wave) wave.style.display = 'none';
        return;
      }

      // Turn ON
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContext();

        // 1. Soothing gentle tropical water ripple & soft monsoon trickle
        const bufferSize = audioCtx.sampleRate * 2;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
          const white = Math.random() * 2 - 1;
          data[i] = (lastOut + (0.018 * white)) / 1.02; // Pink-ish gentle stream
          lastOut = data[i];
        }

        const noiseSource = audioCtx.createBufferSource();
        noiseSource.buffer = buffer;
        noiseSource.loop = true;

        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(420, audioCtx.currentTime);

        const gainNode = audioCtx.createGain();
        gainNode.gain.setValueAtTime(0.045, audioCtx.currentTime);

        noiseSource.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        noiseSource.start();

        // 2. Resonant Kerala bronze temple bell chime
        function playTempleChime() {
          if (!audioCtx || audioCtx.state === 'closed') return;
          const freqs = [528, 660, 792, 1056]; // Harmonics of traditional bell
          const baseFreq = freqs[Math.floor(Math.random() * freqs.length)];

          const osc = audioCtx.createOscillator();
          const bellGain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);

          bellGain.gain.setValueAtTime(0.05, audioCtx.currentTime);
          bellGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 3.5);

          osc.connect(bellGain);
          bellGain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 3.6);
        }

        // Play initial chime shortly after clicking
        setTimeout(playTempleChime, 600);
        bellInterval = setInterval(playTempleChime, 8500);

        isAmbientPlaying = true;
        btn.classList.add('active');
        if (text) text.textContent = 'Kerala Ambience: Playing';
        if (wave) wave.style.display = 'inline-flex';
      } catch (err) {
        console.warn('Web Audio Ambient error:', err);
      }
    });
  }

  // 17. Master Initialization
  function init() {
    initNavigation();
    initSearchAndFilters();
    initKeralaCulturalTicker();
    initKeralaHeritageModal();
    initMapFilterTags();
    initKeralaAmbientSound();
    initLeafletMap();
    initHomeMiniMap();
    renderHomeDestPills();
    renderDestQuickList('all');
    renderDestPills();
    renderOpportunityTable();
    initComparator();

    // Update Top KPIs dynamically from master dataset
    const kpiDest = document.getElementById('kpiDestCount');
    if (kpiDest) {
      kpiDest.textContent = destinations.length ? String(destinations.length) : '10';
    }

    let sumVisits2025 = 0;
    let sumVisits2022 = 0;
    let totalAccommodations = 0;
    let totalRestaurants = 0;
    let totalCafes = 0;

    master.forEach(row => {
      const v25 = getVal(row, ['Domestic_Visits_2025']);
      if (v25 > 0) sumVisits2025 += v25;

      const v22 = getVal(row, ['Domestic_Visits_2022', 'Domestic_Visits', 'visits_2022']);
      if (v22 > 0) sumVisits2022 += v22;

      const acc = getVal(row, ['Total_Accommodation_Listings', 'Total_Accommodations']);
      if (acc > 0) {
        totalAccommodations += acc;
      } else {
        totalAccommodations += getVal(row, ['Hotels']) + getVal(row, ['Resorts']) + getVal(row, ['Homestays']) + getVal(row, ['Serviced_Villas']) + getVal(row, ['Houseboats']);
      }

      totalRestaurants += getVal(row, ['Restaurants']);
      totalCafes += getVal(row, ['Cafes']);
    });

    const totalCommercialSupply = totalAccommodations + totalRestaurants + totalCafes;

    const kpiVisits = document.getElementById('kpiVisitsCount');
    if (kpiVisits) {
      const visitsDisplay = sumVisits2025 >= 1000000 
        ? `${(sumVisits2025 / 1000000).toFixed(1)}M+` 
        : (sumVisits2022 >= 1000000 ? `${(sumVisits2022 / 1000000).toFixed(1)}M+` : fmtNumber(sumVisits2025 || sumVisits2022));
      kpiVisits.textContent = visitsDisplay;
      kpiVisits.title = `${fmtNumber(sumVisits2025)} (2025 recorded footfall) | ${fmtNumber(sumVisits2022)} (2022 baseline)`;
    }

    const kpiVisitsSub = document.getElementById('kpiVisitsSub');
    if (kpiVisitsSub && sumVisits2025 > 0 && sumVisits2022 > 0) {
      kpiVisitsSub.textContent = `${(sumVisits2025 / 1000000).toFixed(1)}M Recorded (2025) • ${(sumVisits2022 / 1000000).toFixed(1)}M (2022 Baseline)`;
    }

    const kpiBiz = document.getElementById('kpiBizCount');
    if (kpiBiz) {
      kpiBiz.textContent = fmtNumber(totalCommercialSupply);
      kpiBiz.title = `${fmtNumber(totalAccommodations)} Stays, ${fmtNumber(totalRestaurants)} Restaurants, ${fmtNumber(totalCafes)} Cafes`;
    }

    const kpiBizSub = document.getElementById('kpiBizSub');
    if (kpiBizSub && totalAccommodations > 0) {
      kpiBizSub.textContent = `${fmtNumber(totalAccommodations)} Stays • ${fmtNumber(totalRestaurants)} Dining • ${fmtNumber(totalCafes)} Cafes`;
    }

    // Event listeners for Home Page controls
    const trendSelect = document.getElementById('homeTrendSelect');
    if (trendSelect) {
      trendSelect.addEventListener('change', (e) => {
        homeTrendMode = e.target.value;
        renderHomeTrendChart(currentDestination);
      });
    }

    const spotlightBtn = document.getElementById('homeSpotlightExploreBtn');
    if (spotlightBtn) {
      spotlightBtn.addEventListener('click', () => {
        selectDestination(currentDestination, true);
      });
    }

    const qiBtn = document.getElementById('homeQiDetailsBtn');
    if (qiBtn) {
      qiBtn.addEventListener('click', () => {
        selectDestination(currentDestination, true);
      });
    }

    const bannerSearchBtn = document.getElementById('btnBannerSearch');
    const searchInput = document.getElementById('globalSearchInput');
    if (bannerSearchBtn && searchInput) {
      bannerSearchBtn.addEventListener('click', () => {
        const q = searchInput.value.trim().toLowerCase();
        const found = destinations.find(d => d.toLowerCase().includes(q));
        if (found) {
          selectDestination(found, false);
        }
      });
    }

    // Invalidate map sizes on window resize
    window.addEventListener('resize', () => {
      if (homeMiniMap) homeMiniMap.invalidateSize();
      if (leafletMap) leafletMap.invalidateSize();
    });

    // Select Munnar as the default initial destination
    selectDestination(currentDestination, false);
  }

  // Kickstart after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
