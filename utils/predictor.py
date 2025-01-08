import pickle

def predict_color(rgb):
    try:
        model_file = "model/color_knn_model.pkl"
        with open(model_file, "rb") as f:
            knn = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {model_file} not found. Train the model first.")
        return None
    
    label = knn.predict([rgb])
    return label[0]