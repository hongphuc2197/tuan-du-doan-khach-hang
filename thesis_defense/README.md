# 🎓 THESIS DEFENSE MATERIALS
## Hệ Thống Dự Đoán Khách Hàng Tiềm Năng Cho Nền Tảng Giáo Dục

**Organized for Master Thesis Defense**

---

## 📁 PROJECT STRUCTURE

```
thesis_defense/
│
├── documentation/          # 📚 Tài liệu chính
│   ├── BAT_DAU_O_DAY.md                    # ⭐ Bắt đầu từ đây
│   ├── CHECKLIST_1_TUAN.md                 # Checklist 7 ngày
│   ├── KE_HOACH_1_TUAN.md                  # Kế hoạch chi tiết
│   ├── SO_SANH_BASELINE_VS_ADVANCED.md     # So sánh models
│   ├── MASTER_THESIS_DOCUMENTATION.md      # Tài liệu đầy đủ
│   ├── LITERATURE_REVIEW.md                # Tổng quan lý thuyết
│   └── README.md                           # Hướng dẫn chung
│
├── slides/                 # 🎤 Slides trình bày
│   └── SLIDES_TRINH_BAY_THAC_SI.md         # 40 slides hoàn chỉnh
│
├── reports/                # 📊 Báo cáo kết quả
│   ├── BOOK_TYPE_ANALYSIS_REPORT.md        # Phân tích loại sách
│   ├── SUMMARY.md                          # Tóm tắt dự án
│   ├── RUN_RESULTS.md                      # Kết quả chạy
│   └── QUICK_START.md                      # Hướng dẫn nhanh
│
├── source_code/            # 💻 Source code chính
│   ├── analytics/                          # ML & Analytics
│   │   ├── analyze_student_data.py         # Phân tích dữ liệu
│   │   ├── predict_potential_customers.py  # Dự đoán khách hàng
│   │   ├── advanced_ml_pipeline.py         # Advanced ML
│   │   └── statistical_analysis.py         # Phân tích thống kê
│   │
│   └── web_application/                    # Web Application
│       ├── backend/                        # Node.js Backend
│       └── frontend/                       # React Frontend
│
├── data/                   # 📊 Dữ liệu
│   ├── user_actions_students_576.csv       # Dữ liệu chính
│   ├── book_type_analysis_report.json      # Phân tích sách
│   └── potential_customers_by_book_type.json
│
├── results/                # 📈 Kết quả
│   ├── charts/                             # Biểu đồ
│   │   ├── confusion_matrix.png
│   │   ├── correlation_matrix.png
│   │   ├── eda_plots.png
│   │   ├── feature_importance.png
│   │   ├── model_comparison.png
│   │   └── book_type_analysis.png
│   │
│   ├── models/                             # Models (sau khi chạy)
│   └── predictions/                        # Predictions (sau khi chạy)
│
└── scripts/                # 🚀 Scripts chạy
    ├── quick_run_for_defense.sh            # ⭐ Chạy nhanh (1-2 giờ)
    ├── run_full_pipeline.sh                # Pipeline đầy đủ
    ├── run_master_thesis_pipeline.sh       # Pipeline thạc sĩ
    └── requirements.txt                    # Dependencies

```

---

## 🚀 QUICK START (Bắt đầu nhanh)

### 1. Đọc Documentation
```bash
cd documentation/
cat BAT_DAU_O_DAY.md
```

### 2. Chạy Script Nhanh
```bash
cd scripts/
chmod +x quick_run_for_defense.sh
./quick_run_for_defense.sh
```

### 3. Xem Slides
```bash
cd slides/
cat SLIDES_TRINH_BAY_THAC_SI.md
```

---

## 📊 KEY RESULTS

**Dataset**: 1,813 records, 576 users, 12 book types
**Best Model**: Stacking Ensemble
**Performance**: F1=89.2%, AUC=94.1%
**Business Impact**: ROI 3.5x, 60% cost reduction

---

## 🎯 FOR THESIS DEFENSE

### Must Read:
1. `documentation/BAT_DAU_O_DAY.md` - Hướng dẫn toàn bộ
2. `slides/SLIDES_TRINH_BAY_THAC_SI.md` - 40 slides
3. `documentation/SO_SANH_BASELINE_VS_ADVANCED.md` - Đóng góp

### Must Run:
```bash
cd scripts/
./quick_run_for_defense.sh
```

### Must Practice:
- Slides 1-40 (15-20 phút)
- Q&A preparation
- Demo web application

---

## 📞 CONTACT

**Author**: [Your Name]
**Email**: [Your Email]
**GitHub**: [Your GitHub]

---

**✅ Ready for Defense!** 🎓🏆
