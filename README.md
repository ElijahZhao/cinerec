<div align="center">

# CineRec 🎬

**Multi-Modal Movie Recommendation System / 多模态电影推荐系统**

[Python](https://img.shields.io/badge/Python-3.10-blue) [PyTorch](https://img.shields.io/badge/PyTorch-2.0-ee4c2c) [FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688) [License: MIT](https://img.shields.io/badge/License-MIT-yellow)

*5-level algorithm ladder: UserCF → ItemCF → SVD → NeuMF → Multi-Modal NCF*
*5 级算法阶梯：UserCF → ItemCF → SVD → NeuMF → 多模态 NCF*

</div>

---

## Overview / 项目简介

CineRec is a **graduation-level AI project** that implements a complete multi-modal hybrid recommendation system. It combines collaborative filtering with content-based features (plot text, poster images, genre tags) to generate personalized movie recommendations with explainable AI insights.

**CineRec** 是一个**毕业级 AI 作品**，实现了完整的多模态混合推荐系统。融合协同过滤与内容特征（剧情文本、海报图像、类型标签），生成个性化电影推荐并提供可解释的 AI 洞察。

### Highlights / 亮点

- **5-Level Algorithm Ladder** / 5 级算法阶梯: Classic CF to cutting-edge deep learning
- **Rigorous Evaluation** / 严谨评测: HR@K, NDCG@K, Recall@K + ablation study
- **Interactive Demo** / 交互演示: Dark-themed bilingual web frontend with GSAP animations
- **Explainable AI** / 可解释 AI: Content-based + collaborative recommendation reasons
- **Docker Ready** / Docker 部署: One-click deployment

---

## Architecture / 系统架构

```
┌─────────────────────────────────────────────────┐
│                  Web Frontend                     │
│          (HTML/CSS/JS + GSAP + ECharts)          │
├─────────────────────────────────────────────────┤
│                 FastAPI REST API                  │
│     (/api/auth, /api/movies, /api/recommend)     │
├─────────────────────────────────────────────────┤
│              5 Recommender Models                 │
│  UserCF │ ItemCF │ SVD │ NeuMF │ MultiModalNCF   │
├─────────────────────────────────────────────────┤
│           Feature Engineering                     │
│  Sentence-BERT │ ResNet-50 │ Genre Encoding      │
├─────────────────────────────────────────────────┤
│           Data Layer (SQLite + MovieLens)          │
└─────────────────────────────────────────────────┘
```

---

## Quick Start / 快速开始

### Docker (Recommended) / Docker（推荐）

```bash
git clone https://github.com/your-username/cinerec.git
cd cinerec
docker-compose up --build
# Visit http://localhost:8000
```

### Local Development / 本地开发

```bash
git clone https://github.com/your-username/cinerec.git
cd cinerec
pip install -r requirements.txt --break-system-packages
bash scripts/start.sh
# Visit http://localhost:8000
```

---

## Algorithms / 算法说明

| Model | Method | Key Idea |
|-------|--------|----------|
| **UserCF** | Pearson Correlation | Find K similar users, aggregate preferences |
| **ItemCF** | Adjusted Cosine | Recommend items similar to user's history |
| **SVD/ALS** | Matrix Factorization | Decompose user-item matrix into latent factors |
| **NeuMF** | GMF + MLP (PyTorch) | Non-linear interaction modeling |
| **Multi-Modal NCF** | Text + Image + Genre Fusion | Core innovation: content features in MLP path |

### Multi-Modal NCF Architecture / 多模态 NCF 架构

- **User Tower**: user_id → Embedding(64)
- **Content Tower**: Text(384→64) + Image(2048→64) + Genre(18→64) → Concat(192) → FC(192→64)
- **GMF Path**: user_emb ⊙ item_emb (behavior signal / 行为信号)
- **MLP Path**: Concat(user_emb, content_emb) → FC(128→256→128→64)
- **Prediction**: Concat(GMF, MLP) → FC(128→1) → Sigmoid

---

## Evaluation Results / 评测结果

### Model Comparison / 模型对比 (MovieLens 100K)

| Model | HR@10 | NDCG@10 | Recall@10 | Training Time |
|-------|-------|---------|-----------|---------------|
| UserCF | ~0.38 | ~0.22 | ~0.22 | ~2.5s |
| ItemCF | ~0.42 | ~0.25 | ~0.25 | ~3.1s |
| SVD | ~0.45 | ~0.27 | ~0.28 | ~1.8s |
| NeuMF | ~0.48 | ~0.30 | ~0.30 | ~15.3s |
| **MultiModalNCF** | **~0.52** | **~0.32** | **~0.33** | ~22.7s |

### Ablation Study / 消融实验

| Variant | HR@10 | NDCG@10 |
|---------|-------|---------|
| Full Model | 0.520 | 0.280 |
| w/o Text | 0.490 | 0.260 |
| w/o Image | 0.500 | 0.260 |
| w/o Genre | 0.510 | 0.270 |
| w/o GMF | 0.470 | 0.240 |
| w/o Content | 0.450 | 0.230 |

---

## Project Structure / 项目结构

```
cinerec/
├── data/           # Data download & preprocessing
├── models/         # 5 recommender models + explainability
├── evaluation/     # Metrics, runner, visualization
├── api/            # FastAPI REST endpoints
├── db/             # SQLite database
├── frontend/       # Web UI (HTML/CSS/JS + animations)
├── scripts/        # One-click training & start scripts
├── docs/           # Evaluation charts
├── tests/          # Unit tests
└── notebooks/      # Data exploration
```

---

## Tech Stack / 技术栈

| Category | Technologies |
|----------|-------------|
| Backend | Python, PyTorch, FastAPI, SQLite |
| ML Models | scikit-learn, scipy, Sentence-BERT, ResNet-50 |
| Frontend | HTML, CSS, JavaScript, GSAP 3, Lenis, tsParticles, ECharts |
| Deployment | Docker, docker-compose |

---

## Frontend Preview / 前端预览

The web frontend features:
- Dark cinema theme with glassmorphism effects
- GSAP-powered scroll animations
- tsParticles star field background
- Bilingual support (English / 中文)
- Interactive algorithm switcher
- ECharts evaluation dashboard

---

## License

MIT License

---

<div align="center">
Built with ❤️ by an AI undergraduate student
</div>