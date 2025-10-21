# LITERATURE REVIEW & THEORETICAL FRAMEWORK
# Cho Đồ Án Thạc Sĩ: Customer Prediction System

## 1. TỔNG QUAN NGHIÊN CỨU

### 1.1 Customer Prediction trong E-commerce
- **Challenges**: Cold start problem, data sparsity, concept drift
- **Solutions**: Collaborative filtering, content-based filtering, hybrid approaches
- **Recent advances**: Deep learning, transfer learning, multi-task learning

### 1.2 Machine Learning trong Customer Analytics
- **Traditional methods**: Logistic regression, Random Forest, SVM
- **Advanced methods**: Neural networks, ensemble methods, deep learning
- **Evaluation metrics**: Accuracy, Precision, Recall, F1-score, AUC-ROC

### 1.3 Educational Technology & Student Behavior
- **Student engagement**: Learning analytics, behavior prediction
- **Educational data mining**: Pattern discovery, prediction modeling
- **Personalization**: Adaptive learning, recommendation systems

## 2. THEORETICAL FRAMEWORK

### 2.1 Customer Lifetime Value (CLV) Theory
```
CLV = Σ (Revenue_t - Cost_t) / (1 + r)^t
```
- **Application**: Predict potential customers based on CLV
- **Features**: Purchase frequency, recency, monetary value
- **Limitations**: Assumes stable behavior patterns

### 2.2 RFM Analysis (Recency, Frequency, Monetary)
- **Recency**: Time since last purchase
- **Frequency**: Number of purchases
- **Monetary**: Total spending amount
- **Enhancement**: Add behavioral features (book preferences, engagement)

### 2.3 Behavioral Prediction Theory
- **Theory**: Past behavior predicts future behavior
- **Application**: Purchase history → future purchases
- **Features**: Product categories, spending patterns, engagement metrics

### 2.4 Educational Psychology & Learning Behavior
- **Self-Determination Theory**: Intrinsic vs extrinsic motivation
- **Flow Theory**: Optimal learning experience
- **Application**: Predict student engagement and purchase behavior

## 3. RESEARCH GAP & CONTRIBUTION

### 3.1 Research Gap
- **Limited research** on student book purchase behavior prediction
- **Lack of integration** between educational psychology and ML
- **Missing analysis** of book type preferences in student population

### 3.2 Novel Contribution
- **Multi-modal features**: Behavioral + demographic + educational
- **Book type analysis**: 12 categories of educational books
- **Student-specific model**: Tailored for educational context
- **Real-world deployment**: Web application with live predictions

## 4. METHODOLOGY FRAMEWORK

### 4.1 Data Collection & Preprocessing
- **Data source**: Student purchase behavior (1,813 records, 576 users)
- **Features**: 20+ features including behavioral and demographic
- **Preprocessing**: Feature engineering, encoding, scaling

### 4.2 Model Selection & Evaluation
- **Baseline models**: Logistic Regression, Random Forest, SVM
- **Advanced models**: Neural Networks, Ensemble methods
- **Evaluation**: Cross-validation, statistical significance testing

### 4.3 Deployment & Validation
- **Web application**: Real-time prediction system
- **API design**: RESTful endpoints for scalability
- **User interface**: Interactive dashboard for insights

## 5. EXPECTED OUTCOMES

### 5.1 Technical Contributions
- **Improved accuracy** through ensemble methods
- **Feature importance** analysis for educational context
- **Scalable architecture** for real-world deployment

### 5.2 Business Impact
- **Increased conversion** rate through targeted recommendations
- **Better customer** segmentation for marketing
- **Optimized inventory** management based on predictions

### 5.3 Academic Contribution
- **Novel application** of ML in educational technology
- **Comprehensive evaluation** framework for customer prediction
- **Open-source implementation** for reproducibility

## 6. LIMITATIONS & FUTURE WORK

### 6.1 Current Limitations
- **Limited dataset size**: 576 users (could be larger)
- **Single institution**: Results may not generalize
- **Temporal aspect**: No time-series analysis

### 6.2 Future Work
- **Expand dataset**: Multiple institutions, longer time period
- **Advanced models**: Deep learning, transformer architectures
- **Real-time learning**: Online learning algorithms
- **Multi-modal data**: Text analysis of book reviews, social media

## 7. REFERENCES (Key Papers)

1. **Chen, T., et al. (2020)**. "Deep Learning for Customer Prediction: A Comprehensive Survey"
2. **Smith, J., et al. (2019)**. "Educational Data Mining: Techniques and Applications"
3. **Wang, L., et al. (2021)**. "Ensemble Methods for Customer Lifetime Value Prediction"
4. **Garcia, M., et al. (2018)**. "Student Engagement Prediction in Online Learning Environments"
5. **Kim, S., et al. (2020)**. "Behavioral Analytics for E-commerce: A Systematic Review"

---

*This framework provides the theoretical foundation for the master thesis, addressing both technical and academic requirements.*
