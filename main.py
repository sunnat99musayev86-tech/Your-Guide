import React, { useState } from 'react';

export default function GrokCinematicStudioExact() {
  const [activeTab, setActiveTab] = useState('imagine');
  const [coins, setCoins] = useState(40); // Стартовый баланс
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(5);
  const [resolution, setResolution] = useState('720p');
  const [isGenerating, setIsGenerating] = useState(false);
  const [history, setHistory] = useState([]);
  
  // Лимит рекламы: ровно на 2 видео самого низкого качества в день (например, 2 * 20 монет = 40 монет)
  const [adsWatchedToday, setAdsWatchedToday] = useState(0);
  const maxAdsPerDay = 2;
  const coinsPerAdReward = 20; // Хватает ровно на 1 низкокачественное видео (5 сек 720p = 20 монет)

  // Расчет цены: Себестоимость API + 20% ваша прибыль (всегда со звуком)
  const calculateCost = () => {
    // 720p со звуком: база ~0.25$ -> 20 монет за 5 сек
    // 1080p FHD со звуком: база ~0.50$ -> 40 монет за 5 сек
    const ratePerSec = resolution === '1080p' ? 8 : 4; 
    return duration * ratePerSec;
  };

  const handleGenerate = (parentId = null) => {
    const cost = calculateCost();
    if (coins < cost) {
      alert('Недостаточно монет! Посмотрите рекламу или купите пакет.');
      return;
    }

    setIsGenerating(true);
    setCoins(coins - cost);

    setTimeout(() => {
      const newNode = {
        id: Date.now(),
        parentId: parentId, // Сохранение цепочки лиц и голоса для продления до 1 часа
        prompt: prompt,
        duration: duration,
        resolution: resolution,
        videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-31918-large.mp4',
      };
      setHistory([newNode, ...history]);
      setIsGenerating(false);
      setPrompt('');
    }, 2000);
  };

  const watchAd = () => {
    if (adsWatchedToday >= maxAdsPerDay) {
      alert('Лимит рекламы исчерпан! Доступно только 2 просмотра в день (хватает ровно на 2 видео низкого качества). Перейдите к покупке тарифов.');
      return;
    }
    setAdsWatchedToday(adsWatchedToday + 1);
    setCoins(coins + coinsPerAdReward);
    alert(`Реклама просмотрена! Зачислено +${coinsPerAdReward} монет.`);
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans max-w-md mx-auto border-x border-gray-900 flex flex-col justify-between select-none">
      
      {/* Шапка 1 в 1 Grok */}
      <div className="border-b border-gray-800 p-4 flex justify-between items-center bg-black/90 backdrop-blur sticky top-0 z-50">
        <div className="font-black tracking-wider text-base">
          GROK <span className="text-gray-400 font-light">CINEMA STUDIO</span>
        </div>
        <div className="flex items-center gap-2 bg-gray-900 border border-gray-800 px-3 py-1 rounded-full text-xs">
          <span className="text-yellow-400 font-bold">🪙 {coins}</span>
          <button onClick={() => setActiveTab('shop')} className="text-white font-bold hover:text-gray-300">+</button>
        </div>
      </div>

      {/* Основной контент */}
      <div className="p-4 flex-1 overflow-y-auto space-y-4">
        
        {/* Вкладка 1: Спросить */}
        {activeTab === 'ask' && (
          <div className="space-y-4">
            <div className="bg-gray-900/40 border border-gray-800 p-3 rounded-2xl text-xs text-gray-300 leading-relaxed">
              Привет! Я ваш ИИ-ассистент Grok. Создавайте концепты сценариев и раскадровки для вашего фильма.
            </div>
            <div className="flex gap-2">
              <input type="text" placeholder="Спросить сценарий..." className="flex-1 bg-gray-900 border border-gray-800 rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-gray-600 text-white" />
              <button className="bg-white text-black font-semibold px-4 py-2 rounded-xl text-xs">Спросить</button>
            </div>
          </div>
        )}

        {/* Вкладка 2: Imagine (Генерация со звуком и продление) */}
        {activeTab === 'imagine' && (
          <div className="space-y-4">
            <textarea
              className="w-full bg-gray-900 border border-gray-800 rounded-2xl p-3 text-xs focus:outline-none focus:border-gray-600 placeholder-gray-600 resize-none text-white"
              rows="3"
              placeholder="Опишите сцену... (лицо и голос героев сохранятся в истории при продлении до 1 часа)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />

            {/* Настройки качества (всегда со звуком, цена зависит от параметров) */}
            <div className="bg-gray-900/50 border border-gray-800 p-3 rounded-2xl space-y-3 text-xs">
              <div className="flex justify-between items-center text-gray-400">
                <span>Длительность:</span>
                <select value={duration} onChange={(e) => setDuration(Number(e.target.value))} className="bg-black border border-gray-800 rounded-lg px-2 py-1 text-white">
                  <option value={3}>3 сек</option>
                  <option value={5}>5 сек</option>
                  <option value={10}>10 сек</option>
                </select>
              </div>

              <div className="flex justify-between items-center text-gray-400">
                <span>Качество (со звуком):</span>
                <div className="flex gap-1">
                  <button onClick={() => setResolution('720p')} className={`px-2.5 py-1 rounded-lg font-medium ${resolution === '720p' ? 'bg-white text-black' : 'bg-black text-gray-400'}`}>720p (Эконом)</button>
                  <button onClick={() => setResolution('1080p')} className={`px-2.5 py-1 rounded-lg font-medium ${resolution === '1080p' ? 'bg-white text-black' : 'bg-black text-gray-400'}`}>1080p FHD</button>
                </div>
              </div>
            </div>

            <button
              onClick={() => handleGenerate(null)}
              disabled={isGenerating || !prompt.trim()}
              className="w-full bg-white hover:bg-gray-200 text-black font-semibold py-3 rounded-2xl transition-all disabled:opacity-50 text-xs"
            >
              {isGenerating ? 'Генерация кадра (со звуком)...' : `Создать видео (${calculateCost()} 🪙)`}
            </button>

            {/* Лента истории с продлением */}
            <div className="space-y-3 pt-4 border-t border-gray-900">
              <h3 className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">История и продление сцен (до 1 часа)</h3>
              {history.map((item) => (
                <div key={item.id} className="bg-gray-900/40 border border-gray-800 rounded-2xl p-3 space-y-2">
                  <video src={item.videoUrl} controls className="w-full h-40 object-cover rounded-xl bg-black" />
                  <p className="text-xs text-gray-300">"{item.prompt}"</p>
                  <div className="flex justify-between items-center pt-2">
                    <span className="text-[10px] text-gray-400 font-mono">{item.resolution} + Звук</span>
                    <button
                      onClick={() => handleGenerate(item.id)}
                      className="bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs px-3 py-1.5 rounded-xl font-medium border border-gray-700"
                    >
                      🔗 Продлить (+{duration}с, лица/голос сохранены)
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Вкладка 3: Сборка */}
        {activeTab === 'assembly' && (
          <div className="space-y-4 text-center py-12">
            <div className="text-gray-400 text-xs">Склейка продленных сцен в единый фильм до 1 часа.</div>
            <button className="bg-gray-900 border border-gray-800 px-4 py-2 rounded-xl text-xs text-white font-medium">Экспорт фильма</button>
          </div>
        )}

        {/* Вкладка 4: Монеты и тарифы (IAP + Лимитная реклама) */}
        {activeTab === 'shop' && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-gray-300 uppercase tracking-wider">Пополнение баланса и реклама</h3>
            
            {/* Реклама с жестким лимитом (ровно на 2 видео низкого качества) */}
            <div className="bg-gray-900 border border-gray-800 p-3 rounded-2xl flex justify-between items-center">
              <div>
                <div className="text-xs font-semibold">Бесплатный бонус (Реклама)</div>
                <div className="text-[10px] text-gray-400">Доступно: {maxAdsPerDay - adsWatchedToday} из {maxAdsPerDay} в день (хватает на 2 видео 720p)</div>
              </div>
              <button 
                onClick={watchAd} 
                disabled={adsWatchedToday >= maxAdsPerDay}
                className="bg-white text-black disabled:opacity-30 text-xs px-3 py-1.5 rounded-xl font-semibold"
              >
                Смотреть
              </button>
            </div>

            {/* 3 тарифа (Себестоимость + 20% маржа + локальные цены) */}
            <div className="space-y-2">
              <div className="bg-gray-900 border border-gray-800 p-3 rounded-2xl flex justify-between items-center">
                <div>
                  <div className="text-xs font-bold text-white">📦 Пакет «Старт»</div>
                  <div className="text-[10px] text-gray-400">300 монет (для тестов и коротких сценок)</div>
                </div>
                <button className="bg-white text-black text-xs font-bold px-3 py-1.5 rounded-xl">$1.99 / 25,000 UZS</button>
              </div>

              <div className="bg-gray-900 border border-gray-700 p-3 rounded-2xl flex justify-between items-center">
                <div>
                  <div className="text-xs font-bold text-white">🎬 Пакет «Режиссер»</div>
                  <div className="text-[10px] text-gray-400">1,000 монет (Основной выбор)</div>
                </div>
                <button className="bg-white text-black text-xs font-bold px-3 py-1.5 rounded-xl">$5.99 / 75,000 UZS</button>
              </div>

              <div className="bg-gray-900 border border-gray-800 p-3 rounded-2xl flex justify-between items-center">
                <div>
                  <div className="text-xs font-bold text-white">🎥 Пакет «Blockbuster»</div>
                  <div className="text-[10px] text-gray-400">3,500 монет (Для фильмов до 1 часа)</div>
                </div>
                <button className="bg-white text-black text-xs font-bold px-3 py-1.5 rounded-xl">$14.99 / 185,000 UZS</button>
              </div>
            </div>
          </div>
        )}

      </div>

      {/* Нижняя навигация Grok */}
      <div className="border-t border-gray-800 bg-black p-2 flex justify-around text-xs text-gray-500 sticky bottom-0">
        <button onClick={() => setActiveTab('ask')} className={`py-2 px-3 rounded-xl ${activeTab === 'ask' ? 'text-white bg-gray-900' : 'hover:text-gray-300'}`}>Спросить</button>
        <button onClick={() => setActiveTab('imagine')} className={`py-2 px-3 rounded-xl ${activeTab === 'imagine' ? 'text-white bg-gray-900' : 'hover:text-gray-300'}`}>Imagine</button>
        <button onClick={() => setActiveTab('assembly')} className={`py-2 px-3 rounded-xl ${activeTab === 'assembly' ? 'text-white bg-gray-900' : 'hover:text-gray-300'}`}>Сборка</button>
        <button onClick={() => setActiveTab('shop')} className={`py-2 px-3 rounded-xl ${activeTab === 'shop' ? 'text-white bg-gray-900' : 'hover:text-gray-300'}`}>Монеты</button>
      </div>

    </div>
  );
}

