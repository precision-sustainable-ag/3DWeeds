# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details
# examples/Python/Basic/pointcloud_plane_segmentation.py
import numpy as np
import open3d as o3d
from matplotlib import pyplot as plt
import copy
from plyfile import PlyData, PlyElement

############################
#Step 1: Initial segmentation / Rotation
############################

if __name__ == "__main__":
    pcd = o3d.io.read_point_cloud('C:\\Users\\Robert Mayo\\PycharmProjects\\OpenCV2\\bag_files\\19700101_122305.bag_ply2.ply')
    print(
        "Find the plane model and the inliers of the largest planar segment in the point cloud."
    )
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.02,
                                             ransac_n=3,
                                             num_iterations=250)

    [a, b, c, d] = plane_model
    print(f"Plane model: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")


# Initial Ransac to find the ground plane
    inlier_cloud = pcd.select_down_sample(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_down_sample(inliers, invert=True)
    outlier_cloud.paint_uniform_color([0, 0.4, 0])
    #o3d.visualization.draw_geometries([pcd])
    #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
    # center = pcd.get_center
    # angle = 180 - np.arccos((a * center[0])/(np.sqrt(a**2 + b**2 + c**2) * center[0]))
    # rotation = -angle

# Convert PCD to numpy array
    #print(float(a)+float(b))
    xyz = np.asarray(pcd.points)
    norm = np.asarray(pcd.normals)
    xyz_in = np.asarray(inlier_cloud.points)
    xyz_out = np.asarray(outlier_cloud.points)

# Find the coordinates of center and angle for rotating the plane
    center = pcd.get_center()
    #print("center: ", center)
    R = pcd.get_rotation_matrix_from_xyz((b, -a, 0))
    # print(R)
    pcd.rotate(R, center=True)
    #R2 = pcd.get_rotation_matrix_from_xyz((0, -a, 0))
    #o3d.visualization.draw_geometries([pcd])
    rgb = np.asarray(pcd.colors)


#############################
#Step 2: Isolate White Square
#############################

# Set the threshold to identify white pixels in color array
    white_0 = np.where(rgb[:,0] < 0.85, 0, 1)
    white_1 = np.where(rgb[:,1] < 0.85, 0, 1)
    white_2 = np.where(rgb[:,2] < 0.85, 0, 1)

# Generate array of xyz information for the white points
    white_tuple = (white_0, white_1, white_2)
    white = np.vstack(white_tuple)
    white_t = white.transpose()
    #white_2d = np.atleast_2d(rgb)
    #white_mult = white.transpose()
    white_pos = white_t * xyz
    #print("size of white array", len(white_pos))
    #print(white_pos)

# Eliminate points clearly outside of the
    elim_above_z = np.where(white_pos[:,2] > (np.median(xyz_in[:,2], axis=0) + np.std(xyz_in[:,2], axis=0)),0,1)
    elim_below_z = np.where(white_pos[:,2] < (np.median(xyz_in[:,2], axis=0) - np.std(xyz_in[:,2], axis=0)), 0, 1)
    #elim_above_y = np.where(white_pos[:, 1] > (np.median(white_pos[:, 1], axis=0) + (np.std(white_pos[:, 1], axis=0))), 0, 1)
    #elim_below_y = np.where(white_pos[:, 1] < (np.median(white_pos[:, 1], axis=0) - (np.std(white_pos[:, 1], axis=0))), 0, 1)
    #elim_above_x = np.where(white_pos[:, 0] > (np.median(white_pos[:, 0], axis=0) + (np.std(white_pos[:, 0], axis=0))), 0, 1)
    #elim_below_x = np.where(white_pos[:, 0] < (np.median(white_pos[:, 0], axis=0) - (np.std(white_pos[:, 0], axis=0))), 0, 1)
    elim_z = elim_above_z * elim_below_z
    #elim_y = elim_above_y * elim_below_y
    #elim_x = elim_above_x * elim_below_x
    #elim = elim_x * elim_y * elim_z
    elimz_2d = np.atleast_2d(elim_z)
    elimz_t = elimz_2d.transpose()
    white_square = elimz_t * white_pos

    #top_corner = [np.max(white_square[:,0],axis=0),np.max(white_square[:,1],axis=0),np.median(xyz_in[:,2], axis=0)]
    #bottom_corner = [np.min(white_square[:,0],axis=0),np.min(white_square[:,1],axis=0),np.median(xyz_in[:,2], axis=0)]

    #np.sort(white_square[:,1], axis=0)
    #print(white_square[:,1])

# Sort the white square X/Y points
    xsort = np.sort(white_square[:,0], axis=0)
    ysort = np.sort(white_square[:,1], axis=0)
    xsort_no_zero = xsort[xsort != 0]
    ysort_no_zero = ysort[ysort != 0]
    xlen = len(xsort_no_zero)
    ylen = len(ysort_no_zero)

# Find the Upper and lower 5th of X/Y points as the sides of the square
# Assumption: top 1/4 of x points will correspond to the right x side, etc. Top 1/5 eliminates outlier pts.
    xupper = xsort_no_zero[int(xlen/5)*4:(xlen-1)]
    xlower = xsort_no_zero[0:int(xlen/5)]
    yupper = ysort_no_zero[int(ylen/5)*4:(ylen-1)]
    ylower = ysort_no_zero[0:int(ylen/5)]

    #print(len(xupper))
    #print(len(xlower))
    #print(len(yupper))
    #print(len(ylower))
    #print("SD Xupper", np.std(xupper))
    #print("SD Xlower", np.std(xlower))
    #print("SD Yupper", np.std(yupper))
    #print("SD Ylower", np.std(ylower))
    #print("Med Xupper", np.median(xupper))
    #print("Med Xlower", np.median(xlower))
    #print("Med Yupper", np.median(yupper))
    #print("Med Ylower", np.median(ylower))

    counts, bins = np.histogram(xupper)
    plt.hist(bins[:-1], bins, weights=counts)
    #plt.show()
    counts, bins = np.histogram(xlower)
    plt.hist(bins[:-1], bins, weights=counts)
    #plt.show()

# Set Minimum and Maximum X/Y values for boundaries of the white square
    x_max = np.where(xyz[:, 0] > (np.median(xupper) + np.std(xupper)), 0, 1)
    x_min = np.where(xyz[:, 0] < (np.median(xlower) - np.std(xlower)), 0, 1)
    y_max = np.where(xyz[:, 1] > (np.median(yupper) + np.std(yupper)), 0, 1)
    y_min = np.where(xyz[:, 1] < (np.median(ylower) - np.std(ylower)), 0, 1)

# Convert matrix for easy calculation
    xmax_2d = np.atleast_2d(x_max)
    xmax_t = xmax_2d.transpose()
    ymax_2d = np.atleast_2d(y_max)
    ymax_t = ymax_2d.transpose()
    xmin_2d = np.atleast_2d(x_min)
    xmin_t = xmin_2d.transpose()
    ymin_2d = np.atleast_2d(y_min)
    ymin_t = ymin_2d.transpose()

# Eliminate everything outside of the square then eliminate the zeros
    elim_max = xmax_t * ymax_t
    elim_min = xmin_t * ymin_t
    elim_outside = elim_max * elim_min
    #elimout_2d = np.atleast_2d(elim_outside)
    #elimout_t = elimout_2d.transpose()
    inside_square = elim_outside * xyz
    norms = elim_outside*norm
    colors = elim_outside*rgb
    just_inside_square = inside_square[inside_square[:, 2] != 0]
    #pcd_norms = norms[norms[:, 2] != 0]
    #pcd_rgb = colors[colors[:, 2] != 0]
    #print(len(just_inside_square))

# Visualize the new Point Cloud inside the White PVC Square
    pcd_white_pos = o3d.geometry.PointCloud()
    pcd_white_pos.points = o3d.utility.Vector3dVector(just_inside_square)
    #pcd_white_pos.normals = o3d.utility.Vector3dVector(pcd_norms)
    #pcd_white_pos.colors = o3d.utility.Vector3dVector(pcd_rgb)
    pcd_white_pos.paint_uniform_color([0.4, 0.4, 0.4])
    #o3d.visualization.draw_geometries([pcd_white_pos])


###################################
# Step 3: Select Distance Threshold
###################################

# Initialize Variables for Dist Threshold Loop
    dist = .01

    sd_in = []
    sd_out = []
    sd_diff = []
    zr_in = []
    zr_out = []
    zr_diff = []
    centers = []
    in_med = []
    out_med = []
    zout_min = []

    range_below_med = []
    range_above_med = []
    sd_below_med = []
    sd_above_med = []
    inlier_range = []
    min_z = []
    dist_l = []
    total_pts = []
    plant_pts = []
    plant_matrix = []
    ground_matrix = []
    out_matrix = []


# Loop through the distance threshold values
# Choose the threshold that most accurately identifies the ground plane

    while(dist < 0.07):
        plane_model, inliers = pcd_white_pos.segment_plane(distance_threshold=dist,
                                                  ransac_n=3,
                                                  num_iterations=250)

        [a, b, c, d] = plane_model
        #print(f"Plane model: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

        inlier_cloud = pcd_white_pos.select_down_sample(inliers)
        inlier_cloud.paint_uniform_color([1.0, 0, 0])
        outlier_cloud = pcd_white_pos.select_down_sample(inliers, invert=True)
        outlier_cloud.paint_uniform_color([0, 0.4, 0])
        #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

        xyz_in = np.asarray(inlier_cloud.points)
        xyz_out = np.asarray(outlier_cloud.points)


    # If array is empty, fill it in with zeros to avoid program errors
        if len(xyz_out) == 0:
            xyz_out = np.array(([0,0,0], [0,0,0]))

    # Calculate the center, min/max and standard dev of the ground and plants
        imed = np.median(xyz_in, axis=0)
        omed = np.median(xyz_out, axis=0)

        sd_inarr = np.std(xyz_in, axis=0)
        sd_outarr = np.std(xyz_out, axis=0)

        max_in = np.max(xyz_in, axis=0)
        max_out = np.max(xyz_out, axis=0)
        min_in = np.min(xyz_in, axis=0)
        min_out = np.min(xyz_out, axis=0)

    # Save relevant data for each iteration of loop in an array
        zr_in.append(max_in[2] - min_in[2])
        zr_out.append(max_out[2] - min_out[2])
        zr_diff.append((max_out[2] - min_out[2]) - (max_in[2] - min_in[2]))
        sd_in.append(sd_inarr[2])
        sd_out.append(sd_outarr[2])
        sd_diff.append(sd_outarr[2] - sd_inarr[2])
        in_med.append(imed[2])
        out_med.append(omed[2])

    # Eliminate points above the median to identify the outliers below the ground
        out_below_med = np.where(xyz_out[:,2] > np.median(xyz_in[:,2], axis=0), 0, 1)
        below_med_2d = np.atleast_2d(out_below_med)
        below_id = below_med_2d.transpose()
        below_matrix = below_id * xyz_out

        if len(below_matrix[below_matrix[:,2] != 0]) == 0:
            max_b = np.array([0,0,1])
            min_b = np.array([0,0,1])
        else:
            max_b = np.max(below_matrix[below_matrix[:,2] != 0], axis=0)
            min_b = np.min(below_matrix[below_matrix[:,2] != 0], axis=0)

        range_below_med.append(max_b[2] - min_b[2])
        sd_below_med.append(np.std(below_matrix))

    # Eliminate points below the median to find range/standard dev of plant region
        out_above_med = np.where(xyz_out[:, 2] < imed[2], 0, 1)
        above_med_2d = np.atleast_2d(out_above_med)
        above_id = above_med_2d.transpose()
        above_matrix = above_id * xyz_out

        if len(below_matrix[below_matrix[:,2] != 0]) == 0:
            max_b = np.array([0,0,1])
            min_b = np.array([0,0,1])
        else:
            max_a = np.max(above_matrix[above_matrix[:,2] != 0], axis=0)
            min_a = np.min(above_matrix[above_matrix[:,2] != 0], axis=0)

        range_above_med.append(max_a[2] - min_a[2])
        sd_above_med.append(np.std(above_matrix))

    # Eliminate zeros in the plant matrix
        no_zeros = above_matrix[above_matrix[:,2] != 0]

    # Save plant and ground matrices to be used in next step
        plant_pts.append(len(no_zeros[:,2]))
        plant_matrix.append(no_zeros)
        ground_matrix.append(xyz_in)
        out_matrix.append(xyz_out[:,2])

    # Save other measures for later steps
        total_pts.append(len(xyz_in[:, 2]) + len(xyz_out[:, 2]))
        inlier_range.append(max_in[2] - min_in[2])
        min_z.append(np.min(xyz_out[:,2]))

    # Save Distance Thresholds
        dist_l.append(dist)

    # Increment distance threshold
        dist = dist + 0.01
    # End Loop


# Print Relevant statistical information that can be used to determine best distance threshold

    #print("dist_l: ", dist_l)
    #print("in med ", in_med)
    #print("zr in: ",zr_in)
    #print("zr out: ",zr_out)
    #print("sd diff: ",sd_diff)
    #print("zr diff: ",zr_diff)
    #print("range above med: ", range_above_med)
    #print("range below med: ", range_below_med)
    #print("inlier range: ", inlier_range)
    #print("sd above med: ", sd_above_med)
    #print("sd below med: ", sd_below_med)
    #print("inlier sd: ", sd_in)


# Set the distance threshold, we later use it to retrieve the relevant data
    dist_thresh = in_med.index(min(in_med))

# Ground reference determines if the segmented plane is actually the ground
    if (range_below_med[dist_thresh] < inlier_range[dist_thresh]) & (range_below_med[dist_thresh] < range_above_med[dist_thresh]):
        ground_ref = 1
    else:
        ground_ref = 0

# If the ground cannot be determined, count all points as plants. Otherwise count segmented plants.
    if ground_ref == 0:
        biomass = total_pts[dist_thresh]
    else:
        biomass = plant_pts[dist_thresh]

    print("distance threshold: ", (dist_thresh*.01)+0.01)
    print("Plant points: ", biomass)
    print("ground reference: ", bool(ground_ref))
    print("total points", len(xyz[:,2]))


#####################################################
# Step 4: Final Segmentation within Region of Interest
#####################################################

    plane_model, inliers = pcd_white_pos.segment_plane(distance_threshold=((dist_thresh*0.01)+0.02),
                                                       ransac_n=3,
                                                       num_iterations=250)

    [a, b, c, d] = plane_model
    #print(f"Plane model: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    inlier_cloud = pcd_white_pos.select_down_sample(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd_white_pos.select_down_sample(inliers, invert=True)
    outlier_cloud.paint_uniform_color([0, 0.4, 0])
    #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

    #o3d.geometry.compute_point_cloud_convex_hull(outlier_cloud)
    #o3d.visualization.draw_geometries(convex_hull)

# Access plant and ground array's from the segmentation
    plant_array = plant_matrix[dist_thresh]
    ground_array = ground_matrix[dist_thresh]
    num_ground_pts = len(ground_matrix[dist_thresh])
    num_plant_pts = len(plant_matrix[dist_thresh])

    #print("highest ground", np.max(ground_array[:,2]))
    #print("median ground", np.median(ground_array[:, 2]))
    #print("highest plant", np.max(plant_array[:,2]))
    #print("lowest plant", np.min(plant_array[:, 2]))

# Plot a histogram of the heights of each plant point
    counts, bins = np.histogram(plant_array[:,2])
    plt.hist(bins[:-1], bins, weights=counts)
    #plt.show()

# Find the sides of the square and find a conversion from Open3D units to cm, using the known side length
    x_side = np.max(ground_array[:,0]) - np.min(ground_array[:,0])
    y_side = np.max(ground_array[:,1]) - np.min(ground_array[:,1])
    median_ground = np.median(ground_array[:,2])
    conversion = 50/((x_side+y_side)/2)

# Check that each side is similar length, should be almost the same
    #print("x side length", x_side)
    #print("y side length", y_side)


# Estimate plant volume from average height, square area, and ground coverage.
    area = (x_side*conversion) * (y_side*conversion)
    avg_z = np.mean(plant_array[:,2])
    avg_plant_height = avg_z - median_ground
    height_cm = avg_plant_height * conversion

    total_coverage = num_plant_pts/(num_ground_pts+num_plant_pts)
    volume_estimation = avg_plant_height * area * total_coverage

# Print average height and ground coverage along with estimated volume for a sanity check on results.
    print("height cm", height_cm)
    print("estimated volume", volume_estimation)
    print("coverage", total_coverage)
