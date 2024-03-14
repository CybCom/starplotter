def on_get_frame(frame, timestamp):
    print('Got frame at', timestamp)
    # Do something with the frame
    # cv2.imwrite('temp/' + str(i) + 'image.png', frame)