import cv2
import numpy as np
from sklearn.cluster import KMeans

# Let's assume you already have a list of points
points = np.array([[100, 200], [110, 190], [400, 400], [410, 410], [450, 450], [120, 210]])

# Define the number of clusters (K)
k = 2

# Apply KMeans clustering
kmeans = KMeans(n_clusters=k)
kmeans.fit(points)

# Get the cluster centers and labels for each point
centers = kmeans.cluster_centers_
labels = kmeans.labels_

# Print the cluster assignments for each point
for point, label in zip(points, labels):
    print(f"Point {point} is in cluster {label}")

# Output the cluster centers
print(f"Cluster Centers: {centers}")

# Optionally, visualize the result
image = np.zeros((500, 500, 3), dtype=np.uint8)

# Assign different colors to different clusters
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Blue, Green, Red (for different clusters)
for point, label in zip(points, labels):
    cv2.circle(image, tuple(point), 5, colors[label], -1)

# Display the image
cv2.imshow('Clusters', image)
cv2.waitKey(0)
cv2.destroyAllWindows()