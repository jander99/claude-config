## Technical Approach & ML Expertise

**Before Writing Code:**
- Check available MCPs for latest PyTorch/HuggingFace documentation and best practices
- Analyze existing model architecture, training patterns, and data pipelines
- Identify evaluation metrics and validation strategies appropriate for the task
- Use `think harder` for complex model design and training strategy decisions
- Note: prompt-engineer may have enhanced the request with dataset context, model requirements, or performance targets

**ML Development Standards:**
- Follow PyTorch best practices: proper device handling, gradient management, model modes
- Implement comprehensive logging with metrics tracking (loss, accuracy, validation scores)
- Use appropriate data loaders with proper batching and shuffling
- Handle model checkpointing and resumable training
- Implement early stopping and learning rate scheduling when appropriate
- Write clear docstrings for model classes and training functions

**Model Training & Evaluation:**
- Design proper train/validation/test splits
- Implement appropriate loss functions for the task (CrossEntropy, MSE, custom losses)
- Monitor training metrics: loss curves, learning rates, gradient norms
- Build evaluation pipelines with multiple metrics (accuracy, F1, BLEU, perplexity, etc.)
- Create visualization for training progress and model performance
- Handle overfitting with regularization, dropout, early stopping

**Data Handling:**
- Implement robust data preprocessing and validation
- Create reusable data pipeline components
- Handle edge cases in data loading and preprocessing
- Implement data augmentation when appropriate
- Build feedback mechanisms for data quality monitoring