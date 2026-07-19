/**
 * CineRec — Dashboard / Model Comparison Page Logic
 */
async function loadDashboard() {
    try {
        const [results, ablation] = await Promise.all([
            CineRec.api('/api/eval/results'),
            CineRec.api('/api/eval/ablation')
        ]);
        renderEvalTable(results);
        renderEvalChart(results);
        renderAblationChart(ablation);
    } catch (err) {
        console.error('Failed to load dashboard data:', err);
    }
}

function renderEvalTable(results) {
    const container = document.getElementById('eval-table');
    const models = ['UserCF', 'ItemCF', 'SVD', 'NeuMF', 'MultiModalNCF'];
    const metrics = ['HR@10', 'NDCG@10', 'Recall@10', 'train_time'];

    let html = `<table class="data-table">
        <thead><tr>
            <th>${CineRec.t('dash.model')}</th>
            <th>${CineRec.t('dash.hr')}</th><th>${CineRec.t('dash.ndcg')}</th><th>${CineRec.t('dash.recall')}</th>
            <th>${CineRec.t('dash.time')}</th>
        </tr></thead><tbody>`;

    models.forEach(model => {
        const data = results[model] || {};
        const isActive = model === 'MultiModalNCF';
        html += `<tr class="${isActive ? 'highlight-row' : ''}">
            <td><span class="model-name gradient-text ${isActive ? '' : ''}">${model}</span></td>
            <td class="metric-cell" data-count="${data['HR@10'] || 0}">${(data['HR@10'] || 0).toFixed(4)}</td>
            <td class="metric-cell" data-count="${data['NDCG@10'] || 0}">${(data['NDCG@10'] || 0).toFixed(4)}</td>
            <td class="metric-cell" data-count="${data['Recall@10'] || 0}">${(data['Recall@10'] || 0).toFixed(4)}</td>
            <td>${data.train_time || '-'}s</td>
        </tr>`;
    });

    html += '</tbody></table>';
    container.innerHTML = html;

    // CountUp for metric cells
    document.querySelectorAll('.metric-cell[data-count]').forEach(el => {
        Animations.countUp(el, parseFloat(el.dataset.count));
    });
}

function renderEvalChart(results) {
    if (typeof echarts === 'undefined') return;
    const chart = echarts.init(document.getElementById('eval-chart'), 'dark');

    const models = ['UserCF', 'ItemCF', 'SVD', 'NeuMF', 'MultiModalNCF'];
    const colors = ['#4a9eff', '#4ade80', '#d4a843', '#a78bfa', '#f87171'];

    chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(20,20,35,0.9)', borderColor: '#d4a843' },
        legend: { data: [CineRec.t('dash.hr'), CineRec.t('dash.ndcg'), CineRec.t('dash.recall')], textStyle: { color: '#8888a0' }, top: 5 },
        grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
        xAxis: { type: 'category', data: models, axisLabel: { color: '#8888a0' }, axisLine: { lineStyle: { color: '#333' } } },
        yAxis: { type: 'value', axisLabel: { color: '#8888a0', formatter: v => v.toFixed(2) }, splitLine: { lineStyle: { color: '#222' } } },
        series: [
            {
                name: CineRec.t('dash.hr'), type: 'bar', barGap: '10%',
                data: models.map(m => results[m]?.['HR@10'] || 0),
                itemStyle: { color: '#d4a843', borderRadius: [4, 4, 0, 0] },
                animationDuration: 1500, animationEasing: 'cubicOut'
            },
            {
                name: CineRec.t('dash.ndcg'), type: 'bar',
                data: models.map(m => results[m]?.['NDCG@10'] || 0),
                itemStyle: { color: '#22d3ee', borderRadius: [4, 4, 0, 0] },
                animationDuration: 1500, animationDelay: 200, animationEasing: 'cubicOut'
            },
            {
                name: CineRec.t('dash.recall'), type: 'bar',
                data: models.map(m => results[m]?.['Recall@10'] || 0),
                itemStyle: { color: '#4ade80', borderRadius: [4, 4, 0, 0] },
                animationDuration: 1500, animationDelay: 400, animationEasing: 'cubicOut'
            }
        ]
    });

    window.addEventListener('resize', () => chart.resize());
}

function renderAblationChart(ablation) {
    if (typeof echarts === 'undefined') return;
    const chart = echarts.init(document.getElementById('ablation-chart'), 'dark');

    const variants = Object.keys(ablation).filter(k => !k.startsWith('_'));
    const hrData = variants.map(v => ablation[v]?.['HR@10'] || 0);
    const ndcgData = variants.map(v => ablation[v]?.['NDCG@10'] || 0);

    chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(20,20,35,0.9)', borderColor: '#d4a843' },
        legend: { data: [CineRec.t('dash.hr'), CineRec.t('dash.ndcg')], textStyle: { color: '#8888a0' }, top: 5 },
        grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
        xAxis: { type: 'category', data: variants, axisLabel: { color: '#8888a0', rotate: 15 }, axisLine: { lineStyle: { color: '#333' } } },
        yAxis: { type: 'value', min: 0.2, axisLabel: { color: '#8888a0', formatter: v => v.toFixed(2) }, splitLine: { lineStyle: { color: '#222' } } },
        series: [
            {
                name: CineRec.t('dash.hr'), type: 'bar',
                data: hrData,
                itemStyle: { color: '#d4a843', borderRadius: [4, 4, 0, 0] },
                animationDuration: 1500, animationEasing: 'cubicOut'
            },
            {
                name: CineRec.t('dash.ndcg'), type: 'bar',
                data: ndcgData,
                itemStyle: { color: '#a78bfa', borderRadius: [4, 4, 0, 0] },
                animationDuration: 1500, animationDelay: 200, animationEasing: 'cubicOut'
            }
        ]
    });

    window.addEventListener('resize', () => chart.resize());
}
