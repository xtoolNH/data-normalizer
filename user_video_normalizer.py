import os
import cv2
import logging
from datetime import datetime, timedelta


def user_video_writer(filename, final_folder, start_date, end_date):
    video_filename = final_folder + '/' + filename + '.mp4'
    start_date = start_date
    end_date = end_date
    # start_date = '2019-05-20 13:19:19'
    # end_date = '2019-05-20 13:19:21'
    image_folder = '../user-video/data/' + filename
    images = []
    ext = '.png'
    logging.basicConfig(filename='logs/' + filename + '.log', level=logging.DEBUG)
    logging.debug('Normalization of User Video starts here')
    logging.info('Start Date:\t' + str(start_date))
    logging.info('End Date:\t' + str(end_date))

    # convert incoming start date and end date in valid datetime format
    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # `XVID` for avi file
    out = cv2.VideoWriter(video_filename, fourcc, 24.0, (640, 480))

    # create video folder
    if not os.path.isdir(final_folder):
        logging.info('Creating Final Folder:\t' + str(final_folder))
        print('Creating Final Folder:\t' + str(final_folder))
        os.mkdir(final_folder)

    for f in os.listdir(image_folder):
        if f.endswith(ext):
            images.append(f)

    # sort all images in ascending order
    logging.info('Sorting all Images in Ascending Order')
    print('Sorting all Images in Ascending Order')
    images.sort()

    # Determine the width and height from the first image
    image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(image_path)
    cv2.imshow('video', frame)
    height, width, channels = frame.shape

    # traverse for each image found within folder
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)

        # remove extension of file
        image_name = image[:-4]
        # convert filename to datetime format
        image_name = datetime.strptime(image_name, '%Y-%m-%d %H.%M.%S.%f')
        # convert datetime format to our desired format for comparision with dates
        image_name = datetime.strftime(image_name, '%Y-%m-%d %H:%M:%S.%f')[:-3]
        # make datetime object
        image_name = datetime.strptime(image_name, '%Y-%m-%d %H:%M:%S.%f')

        end_date_plus_one = end_date + timedelta(seconds=1)

        # compare datetime if between our required datetime
        if (image_name > start_date) and (image_name <= end_date_plus_one):
            logging.info('will store:\t' + str(image_name) + '.png')
            print('will store:\t' + str(image_name) + '.png')
            out.write(frame)  # Write out frame to video
        else:
            logging.info('will skip:\t' + str(image_name) + '.png')
            print('will skip:\t' + str(image_name) + '.png')

        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('exiting while loop because user pressed `q` key')
            logging.debug('exiting while loop because user pressed `q` key')
            break

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()
    logging.debug('Normalization of User Video ends here')
