import os
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pupil_apriltags import Detector



detector = Detector(
                    families="tag36h11",
                    nthreads=4,
                    quad_decimate=2,
                    quad_sigma=0.0,
                    refine_edges=1,
                    decode_sharpening=0.25,
                    debug=0,
                    )
bridge = CvBridge()
pub = rospy.Publisher('/apriltag_detector_image',Image,queue_size=10)

def tag_drawer(cv_image,tags):
    #print(len(tags))
    if len(tags)>0:
        for tag in tags:
            cv2.putText(cv_image,'Tag Detected!!!!!!!!!!!!!!!!!!',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            print('Detected')
            # tag_id = str(tag.tag_id)
            # cv2.line(cv_image,tag.corners[0],tag.corners[1],(0,255,0),2)
            # cv2.line(cv_image,tag.corners[1],tag.corners[2],(0,255,0),2)
            # cv2.line(cv_image,tag.corners[2],tag.corners[3],(0,255,0),2)
            # cv2.line(cv_image,tag.corners[3],tag.corners[0],(0,255,0),2)
            # cv2.putText(cv_image,tag_id,tag.center,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    else:
        #print('No Tag Detected')
        cv2.putText(cv_image,'No Tag Detected',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    #cv2.circle(cv_image,tag.center,5,(0,0,255),-1)
    return cv_image

def tag_callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "rgb8")
    except CvBridgeError as e:
        print(e)
    cv_image_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    tags = detector.detect(cv_image_gray)
    #print('image_detected')
    tag_drawer(cv_image,tags)
    pub.publish(bridge.cv2_to_imgmsg(cv_image, "rgb8")) 
            

def listener():
    rospy.init_node('tag_SubPub',anonymous=True)
    rospy.Subscriber('/stereo_camera',Image,tag_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

                    
                    
                    
