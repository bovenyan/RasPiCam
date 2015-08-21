import cv2
import pdb
from skimage.feature import hog
import copy


def train_face_process(img, detect_reg, clf=None):
    """get dectection images """
    # detection region vector field to specify detection region
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = []
    if not (clf is None):
        """further refinement mode"""
        face_cascade1 = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')
        faces1 = face_cascade1.detectMultiScale(gray, scaleFactor=1.1,
                                                minNeighbors=3,
                                                minSize=(30, 30))
        for face in faces1:
            (x, y, w, h) = face.tolist()
            if x < detect_reg[1] and x > detect_reg[0] and y < detect_reg[3] \
                    and y > detect_reg[2]:
                temp = gray[y:y+h, x:x+w]
                faceImgRe = cv2.resize(temp, (32, 32))
                HoGVec = hog(faceImgRe, orientations=8,
                             pixels_per_cell=(4, 4), cells_per_block=(2, 2))
                pdb.set_trace()
                if int(clf.predict_proba(HoGVec)[0, 1] > 0.2):
                    faces.append([x, y, w, h])
    else:
        """no need to refine results """
        face_cascade1 = cv2.CascadeClassifier('hogcascade_pedestrians.xml')
        faces1 = face_cascade1.detectMultiScale(gray, scaleFactor=1.05,
                                                minNeighbors=10,
                                                minSize=(30, 30))
        for face in faces1:
            (x, y, w, h) = face.tolist()
            if x < detect_reg[1] and x > detect_reg[0] and \
                    y < detect_reg[3] and y > detect_reg[2]:
                temp = gray[y:y+h, x:x+w]
                faces.append([x, y, w, h])
    return faces


def heatMap_proc(file_path, dev_id, cam_id, clf=None):
    """ detection section """
    # assume the only parameter is the filename of the captured frame
    frame = cv2.imread(file_path)
    height, width, n_channels = frame.shape

    # detection region and tracking region
    # this is default value, override later by actual frame size
    detect_reg = [0, 1000, 0, 1000]
    # detect region is always the full frame for mall solution
    detect_reg[1] = int(width)
    detect_reg[3] = int(height)

    # list for recording all 'face':upperbody actually position
    # all_face = []
    heatmap_face = []
    # find new upper body
    new_faces = train_face_process(copy.copy(frame), detect_reg, clf)
    for face in new_faces:
        (x, y, w, h) = face
        faceDict = {}
        faceDict['x'] = int(x+w/2)
        faceDict['y'] = int(y+h/2)
        # v is always 1 for now
        faceDict['v'] = 1
        # all_face.append(face)
        heatmap_face.append(faceDict)
    res = {}
    # save all detected peds to pickle file
    res['device_id'] = dev_id
    res['cam_id'] = cam_id
    res['count'] = len(heatmap_face)
    res['heat_map'] = heatmap_face

    # pkl.dump(dict, open(pklDumpName, 'wb'), -1)
    return res

    """ ploting section """
    # faces = dict['face']
    # for face in faces:
    #     (x,y,w,h) = face
    #     cv2.circle(frame,(int(x+w/2),int(y+h/2)),10,(0,255,0),thickness =-1)

    # cv2.imshow('fret',frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # pdb.set_trace()
