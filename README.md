# Embedded Machine Learning for Posture Detection

## Overview
This project focuses on designing a posture detection system that utilizes sensor data from Arduino to distinguish between various postures. Leveraging TensorFlow and the Edge Impulse platform, this system demonstrates the integration of machine learning into a microcontroller environment, achieving an impressive accuracy of approximately 88.65% on test data.

### Author
- Pranit Sehgal - *Arizona State University* - ASU ID: PVSEHGAL@ASU.EDU

## Features

- **Data Collection**: Utilizes accelerometer, gyroscope, and magnetometer data from Arduino sensors.
- **Machine Learning Model**: Employs a Convolutional Neural Network (CNN) architecture suitable for analyzing time-series sensor data.
- **Real-time Prediction**: Capable of making real-time posture predictions when deployed on Arduino, demonstrating practical applications in health monitoring systems, gaming controls, and ergonomic equipment.


### Data Handling
- **Collection**: Gathered from Arduino's various sensors and stored in CSV format.
- **Cleaning and Aggregation**: Processed using Python scripts in pandas to clean, merge, and prepare data for training.

### Machine Learning
- **Model Architecture**: CNN with Conv1D, MaxPooling, Flattening, and Dense layers, using relu and softmax activation functions.
- **Training**: Utilized the Adam optimizer and sparse_categorical_crossentropy loss function, trained for 50 epochs.

## Results

- **Training and Validation**: Monitored performance across both sets to fine-tune the model.
- **Test Accuracy**: Achieved approximately 88.65% with a loss of 0.3164.
- **Real-time Prediction**: Integrated model into Arduino for live data prediction, with around 70% accuracy in practical applications due to sensor inconsistencies.

## DEMO
https://drive.google.com/file/d/1VVS8PMOueLMXs5onEnYGI6CSPbOLqEiP/view?usp=sharing

### Google Colab Notebooks
1. Machine Learning Model: [View Notebook](https://colab.research.google.com/drive/1IsssGuMVhRPL9l4skXLkncZtRjIxfMSa?usp=sharing)
2. Data Cleaning: [View Notebook](https://colab.research.google.com/drive/1Dx1xko5obV4vSt65snU3PE_1QR-485VS?usp=sharing)

### Setup
- Ensure you have TensorFlow installed.
- Follow the instructions in the provided Google Colab notebooks to train the model and prepare it for deployment.

## Contributing
I welcome contributions from the community to improve the system's accuracy, explore new neural network architectures, or enhance sensor data preprocessing. Please submit a pull request or open an issue for discussion.

## Acknowledgments
- Thanks to Arizona State University for the support and environment conducive to conducting this research.
- TensorFlow and Edge Impulse for the tools that made this project possible.

## Future Directions
- Investigate advanced noise-reduction techniques and sensor replacement to address magnetometer inconsistencies.
- Explore deeper or alternative neural network architectures for improved accuracy.
- Consider integrating additional sensors or data sources for a more robust posture detection system.

## Contact
For further inquiries or to discuss potential collaborations, please reach out to Pranit Sehgal at [insert contact information].
