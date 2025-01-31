import time
import win32gui
import win32process
import psutil
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from datetime import datetime, timedelta
from collections import defaultdict
import csv
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import io
import base64
from pystray import Icon, MenuItem, Menu
from io import BytesIO



class ScreenTimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Time Tracker")
        self.root.config(bg="#4a4a4a")  # Set background color of the window
        # Calculate position for centering the window
        # Get screen width and height to center the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 600
        window_height = 530
        # Set up a minimize button
        icon_base64 = 'AAABAAEAQEAAAAEAIAAoQgAAFgAAACgAAABAAAAAgAAAAAEAIAAAAAAAAEAAABMLAAATCwAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAAAAAAAFBUXANnV0gDl0LUA/OrHAP///wD///8A////AP///wD///8A////AP///wD///8A///3AP//7gD///UAj5WtAAAVWwAILFsACzBkAAwvYAAJK1kABydRZA0pT9UbNVvyJ0Fo8ixGbvIsRm7yJD9m8hgzWPIMKU/LBytgVQkwbgAKL2QACjFoAAkuXQAAFUgAMVJ+AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wC3qZ0AkIR5AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAAAAAAABQVFwDZ1dIA5dC1APzqxwD///8A////AP///wD///8A////AP///wD///8A////AP//9wD//+4A///1AI+VrQAAFVsACCxcAAsxaAAIK1stCCZMvhcxVv8pQmj/NU94/ztVfv8+V4D/PliA/ztUfv80TXb/KUJn/xcwU/8JKFO7BitcKQkzbQAJLl4AABVIADFSfgD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8At6mdAJCEeQD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAAAAAAAUFRcA2dXSAOXQtQD86scA////AP///wD///8A////AP///wD///8A////AP///wD///cA///uAP//9QCPla0AABZcAAcuYAAHKVhgDSlO/x84Xf8wSnL/OVN9/0Fag/9HX4f/SWGI/0lhiP9GX4f/QFmC/zlTfP8xS3L/IDlb/w0oS/4GLF9kCC9gAAAVSQAxUn4A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ALepnQCQhHkA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAAAAAAAFBUXANnV0gDl0LUA/OrHAP///wD///8A////AP///wD///8A////AP///wD///8A///3AP//7gD///UAjpWvAAAVXwAFJk6LEStN/yU9Y/8xS3X/O1V+/0hhif9PZ4//T2eP/09njv9PZo7/T2eP/09njv9IYIj/O1V+/zJMdv8mPmT/EixQ/wYnToQAGE8AL1F+AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wC3qZ0AkIR5AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAAAAAAABMUFgDb2NYA7ti7AP/40AD///8A////AP///wD///8A////AP///wD///8A////AP///wD///sA////AIqTrQAAAEF9CSRH/ypCZ/8xS3T/OlR9/05ljf9SapL/QVyE/zdSef84UXn/OFJ5/zdSef9CXYT/UmqS/0xjjP85U33/Mkx1/ydAZv8TK07/ABFEeTJUggD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AuKufAI+DeAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAAAAAAAAAAAA3NfSAM+6o2HQvqaD2tPNgNrTzYDa08yB2tPNgtrTzYPa082G2tPNh9rTzYja08mJ2tPFitrTzIiwpZ6aTk5d/x03X/8mRXT/PVZ+/1Bnjv9Yb5b/QVuD/zhNd/88TXf/P055/z9Pef87TXf/N013/0Nchf9Zb5b/T2aO/ztVfv8zTnf/Jz9m/wAJNf9SaohN////APv7+wD+/v4A/v7+AP7+/gD+/v4A/v7+AP7+/gD//v4A///+ALOklwCMgXYA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AEpMTgBKTU8AT09PBaiYi7urnZP/qJ6Y/7Wonf+3qZ7/tqme/7apnv+2qZ7/tqmf/7apn/+2qZ//t6qh/7eqo/+0qJ//xLWo/9zGq/+RiIX/NU95/0ZhjP9fdJr/SmGJ/y9Bbf8wPWr/M0Bu/zxLd/88Snf/M0Bu/y89av8wQm7/T2WN/150mv9LY4z/PlmC/zNOd/8QLFf/Jztb/8m+tdfXybzXxLqy18a8s9fGvLPXxryz18a8s9fGu7PXx72018W6stemlonQoJSKb////wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP/37mevoZf/yMG6/9LLxP/UzMf/18/J/9fQyv/X0Mr/19DK/9fQyv/X0Mv/2NHL/9jRy//Y0cv/1M3H/9DJw//Nxb7/48y1/4KGlf8/XY7/WnCW/05kjP9HXYX/SV2F/1lrkv9tf6P/a36i/1lskv9KYIj/SV6H/1Fnj/9bcJf/V22U/0tkjP8+WIH/MUx1/wARQP9ZZXX/8uHQ/8m/t//IwLf/yMC3/8jAt//IwLf/yMC4/8i/t//DurH/wrmy/7qupf////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8Alo6IAJWNhgC4rqaX6+fl/+nl4v/n49//6OPf/+Xg3P/k3tr/5N7a/+Te2//k39r/493Z/+Pd2f/k3tr/5N7a/+bh3f/o4t//6+bk////8f+nqLL/PFiI/11ymP9ec5n/XHOZ/2V7ov9fdZr/PFN3/zhQdP9acJX/Ynmg/1xzmf9fc5n/XnKY/1xxl/9Va5P/SGGK/zlTff8WNF7/BSBI/9rW0///////8Oni/+Da1v/i3Nj/4t3Y/+Ld2f/j3dn/5N7a/+bh3v/k3tv+////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AH1+fwB9fn4AuLazTP/+/v///////f39//j18//t6eb/7Ofl/+zo5v/r5+X/7urn//Pv7f/x7uz/7urn//Dr6f/59/j///////////////3/c4Cc/01lkf9idpv/Ynab/1xymf88VX7/DCpQ/wsoT/8KJ07/DClP/z5XgP9dc5r/Ynab/2N3nP9hdZr/W3CX/09nkP9AW4X/Mkx1/wAVQv9SZX3/0dLW/+nk4f/69fL/7ejm/+3p5//s5+X/8+/u//37/P////////37/////wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD07ORv/Pn67v36+//18e//7urn//Pv7f/28vH/9vLx//by8P/7+Pj//fv7//f08v/38/L////////////Z2d3/fIij/0ZgjP9leZ7/ZXmd/2V5nf9bcpr/HTlh/ylDav9gdZz/YHWc/yZBaP8hPWX/XXOb/2V5nf9leZ3/ZHid/19zmf9TapL/RV+J/zZRe/8jPmX/ABY+/wMfTf9ZbY//9/X0//38+//49fT/9/Tz//z5+v//////////puri3UD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AmZCKAJmQigCZkIkAlYmAAMC1q+fm39r/8Ozq//f08//7+fn//Pv7//37+//9+/z//fv8//z6+//9/Pz//vz8////9/+Znaf/Hjxu/zlVhf9jd5z/aHue/2d6n/9mep7/XXOa/y1Jcv9CXIX/dIaq/3OFqf8/WYP/MEx2/190m/9meZ7/Z3qf/2d6nv9hdZr/VWyT/0dgif85VH//K0Zu/w0pTv8TMlv/FTdr/7W9zf////////7/////////////5uHf7rOtpwCtqKQA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ALOWgQCzloEAs5WAAK2Qe0W7raP/5eHe//r39v////////////////////////////v6+v//////////////////+ub/YmuB/yBDef9Zb5X/Y3eb/2h7n/9qfKD/Z3qe/2F2nP9FXoj/M1B9/01mkf9MZZD/M1B8/0dgiv9hdpz/Z3qf/2p9oP9oe5//Ynab/1dtlP9GYIn/N1N8/y5Jcv8YMlj/Ei1S/xEyZv+cp73w/////////////////////+fi3n+3uLkA0dLSAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wCLgXkAi4F5AIuBeQCIfHMfyLyz//Tw7////f3///////////////////////v5+v///fX/////////////////mpie/yE+bP9DXYj/WG6V/2R4nf9qfqP/a36i/2t9of9jd5z/VmyV/0dhjP9GYIv/RmCL/0hijP9WbZb/Y3ec/2t9oP9ugab/bYGn/2N3nv9Ybpb/SGCJ/ytBY/8tRm7/Hzlg/w8qTv8lQGr/OliIx9nj7TD///+x7ufkzLixqnX9+PIA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AGR0gABkdIAAZHiEAGx4hAMi9tMn89/L///////////////////////////////3/qau1/4mSpf+qrrL/b3aG/xc1Yv8tS3r/RF6K/1tznv90ibL/c4iv/3uPtv9keaH/XHKc/1hwmP9Zb5b/Znqe/2d6nv9Yb5X/WG+X/2B2n/9tgan/coas/26Aov93i7D/Vm6a/z5ZiP84Unr/L0lx/yA7Yf8QK1D/Lkds/xo9dPswU5AA9/HoAP3u3ABra2gA8ezmAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAAAAAAAAAAAAAAAAABYUk0t8+fd///9/f//////////////////////8efh+ipEb/YAD0H/ABI8/wAfTv8pRXD/QF6M/2l/pP9xe43/Ji87/x0iLP86QlD/tLrG/5Wdq/8mQWz/WG+Y/3CCpf9xgqX/VWyV/ypGcf+hqLX/mJ6p/xYbJv8VFhn/Oz9H/4SMmv96jKz/P12N/y5Jcv8eOF//GTRa/x85YP85UXj/AB5mNjdRfgD88dwAopWEAP/26gD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wC4uLgAuLi4ALi4uAC3t7cAt7e3APjz7zXc1M+87ujk//Tu6v/48vDy///4kp6pukcAFEP7MEx1/yM/af8aNFr/ME59/yo9Xf/e187/eXp3/wAAAP8AAAD/AAAA/0tHPv9PXG//JkRx/1Nqkv9oe6D/aXyg/1Jpkv8pRnP/TVtx/yopJP8AAAD/AAAA/wAAAP+cmpX/1Mu8/yc4Vv8wT3//GzVa/yRBa/82UXv/FzBT/x5EeUQAJ24APV2RAIKEiQDt7+4A8/j/APP4/wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8Ao6OjAObi3yH17+pE/Pr4EtjX1gAZPWsKHzto/05jiP8ZMVL+HThh/zVTgv8qPl7/TU1N/yMmKf8yMjL/EREQ/xAXI/8WK03/Lkx7/0Vehv9MY4r/WG2U/1hulP9MY4v/RF2F/zFPfv8fNVj/ISs6/wYJDf8AAAH/LTA1/zk+Rv8rQGP/NVOB/yA8Zv8PIz/9RVt+/zxbi/8pVJUaMmKpABJGlAAkU5gAPGekADlkowA5ZKMA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A/f39AKGiogDx8/QA////AP///wC7vsMAABpwAD561F4vOku1BAwW/SNCb/8vSnL/RGGQ/ytGc/8xRGX/SVt6/0tegf9ac57/W3Wi/0xjiv9EW4P/Rl6F/0lgiP9JYYj/Rl6F/0Nbg/9LYon/XHWh/1x2pP9SaI3/TWCD/zVLcP84Vob/Q2GP/y9Jcf8kQ3H/CRIe/RcdKqdHcbMtN2WnADVfnQA3YZ4AMV6gACRSlgAkUpUAJFKVAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP39/QClpaUA7+/vAP///wD///8A0NLWAAANTQARO3kAEhIQRQ8XI/8iQW3/L0py/ztWgv9JZJL/WHKg/2N7p/9ofqf/YXae/1Zul/9JYYn/QFiA/0BYgP9CWoL/QlqC/0BYgP9AWID/R2CI/1Vtl/9gdp7/ZXuk/2N6pf9WcJz/SGSR/zxYhP8vSnL/I0Fv/xUiNP8GAQCtEBoqABcnPQAVIjYAFSI2ABUiNgAVIjYAFSI2ABUiNgD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A3t3cAP38+wD///8A////AP///wD9/f0ApaWlAOzs7AD///8A////AFlZWwAAAAAAAwAAAAcEAHwTHiz/IkBq/zBMd/81TXL/P1d8/1Brmf9Xcp//WXOg/09okP9DW4H/P1iB/z1Wf/8/V3//QFiB/0BYgP8/V3//PVZ//z5Xf/9BV3z/TGKK/1ZwnP9WcJ7/TWeU/zxSdP81S2//MU14/yNBbf8THSr/DAwK5gUEAgAFAgAABQMAAAUDAAAFAwAABQMAAAUDAAAFAwAA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ACslHQDv4dMA6N3VAPLs6AD///8A////AJ+goQD///8A////AFlaWwAAAAAACw0RAAwOEwAMDg+sERUZ/yI8Yf8zUoH/NEpu/ygwP/8qMkH/MD1S/y05Tv8fJi//FBYW/ys3S/9JY4//SGCI/0dfh/9HX4f/SGCI/0pkkP8tOlD/FBUW/xwgJv8oMkH/KzZH/yUsOP8nLz3/NEtv/zRTgf8kPWL/EBQZ/w4PEP8LDhIpCg4SAAoOEgAKDhIACg4SAAoOEgAKDhIACg4SAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAnIhoA8eLTANO/sADFrJkA5NXKAPLr5gCwsK8A1tncAFBSVQAAAAAACQ0TAA0RFwALDxUADA8TtA8PDP8iNVH/MlF//zlXhP87Unf/LjpM/ykxPf8pMDz/LjhI/zZCVv9FV3X/Vm2V/1Zsk/9XbJL/V2yT/1Zsk/9WbZX/SVt7/zpIX/8zPlH/LDVE/ys1Qv8yQFX/Pld//zpXhf8yUH7/JDlY/xMUFP8PEhX/Cg0SfAsOEgALDhIACw4SAAsOEgALDhIACw4SAAsOEgD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AMSwkAPLk1gDcy78AybOhAM2zoQDOtaMA7NXFAH51bwAAAAAAAwYLAAsPEwAJDREACAsPAA4SFc4ZGBT/JTVM/zFQgP81UHn/QFyJ/05qmf9SbJj/Vm6Z/1p0n/9geaX/Xnaf/1xwlf9gdJn/Ynab/2J2m/9hdJn/XHGW/151nf9geaX/XHWh/1dxnf9Ubpv/TmqZ/0FciP81UHr/MlGB/yY5VP8ZGBb/DxIV/wwQFKYNERUADREUAA0RFAANERQADREUAA0RFAANERQA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ADEsJADy5NYA28q+AMu1pADUvq4A0rysAN7FswDu074AXVZSAAAAAAAEBwsACg4SAAgLDwAUFxrgIR8c/yo3Sv8xT4D/NlF7/z5Ygv9HYIr/T2iQ/1ZslP9acJb/XnKY/2B0mf9jdpv/Znmd/2h7n/9oe5//Znmd/2N3m/9gdJr/XnOY/1twlv9WbJT/UGiR/0hhiv8/WYP/NlJ8/zJSg/8lNUz/GhkW/xMWGv8SFRmjDxMYABAUGAAQFBgAEBQYABAUGAAQFBgAEBQYAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAxLCQA8uTWANvKvgDLtaQA1L6uANO9rQDQuqsA4cm3APvgzQBwZmAAAAAAAAgLEAAMDxQADRAU2RISD/8fKjf/ME58/zhUfv8+WYP/R2CJ/09nkP9YbpX/XnOZ/2J1mv9keJz/Znqe/2l8n/9qfaD/an2g/2l8oP9nep7/ZHic/2J2m/9fc5n/WW+W/1Fokf9IYYr/P1qE/zhUf/8xT37/Iiw8/yAfHP8aHSD/ERUZdw4SFwAPExgADxMYAA8TGAAPExgADxMYAA8TGAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AMSwkAPLk1gDbyr4Ay7WkANS+rgDTva0A072tAM+6qgDhybcA/+zXADo4NwAAAAAACQ0SLQ0QFPgcHh//HSEj/y1Gbf87WYj/PlmE/0dgiv9QaJH/WW+W/2B1mv9jd5z/Znmd/2h8n/9qfKD/a32g/2t9oP9qfKD/aHuf/2Z5nv9kd5z/YXSa/1pwlv9RaZH/SGKL/0BahP88WIT/ME15/x8lLf8kJCT/Fxse/w0QFEkNERYADhEWAA4SFgAOEhcADhIXAA4SFwAOEhcA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ADEsJADy5dcA3Mu/AMu1pADVvq4A1L2tANS9rQDUva0A0burAO7UwQDSvKwAFRUWAAAAAHUYGx7/IyYq/yEfHP8mOVb/PmGV/z9ahP9HYIr/UGiR/1lvlv9fdJr/Y3ec/2Z5nf9oe5//anyg/2t9oP9rfaD/anyg/2h7n/9meZ7/Y3ec/2B0mv9acJb/UmqR/0ljjP9DXoj/RGWa/yc+YP8VFhX/GBsd/xEUF/8MDxRfDBAVAAAAAgAAAAAADBAUAAwQFAAMEBQADBAUAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAqJh4A+OvcAN3LvgDLs6EF1b6sANS8qwDUvKsA1LyrANS8qwDPuKcA+NzHAMq1pgAdGxt0BQkO/yYpLP8mJib/FBgc/y5KdP9LbKD/SmWP/09nkf9Yb5f/X3Sa/2V5nv9rf6X/bYKo/3GFqv9zhqz/coWq/3GFqv9tgqf/an+k/2l9o/9keaD/X3Wd/1hwmv9PaZX/RWWZ/ytIcv8MEBb/CwsK/wsPE/8QExb/DhEUswAAAgAfIycANTU0AAEBAgABAQIAAQECAAEBAgD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8ALikiBNjHt5LDtavav7Ck58GypuDAsabhwLGm4cGxpuHBsabhwLGl4b2uo+Hr18beppqS6hEVGv8eIib/HCAk/wgHBf8KDxT/K0No/0Njlf9ScKH/WnWl/196qP9feKX/W3GZ/1xxlv9ZbZL/WGyR/11xlv9cb5T/XXKY/150nP9QaZP/OFWE/yhIef8YOm3/CCtb/wAQL/8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPkAAAAAwbm1AJeUkAAAAAAAAAAAAAAAAAAAAAAA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AJqPiKG4qJ3/wLev/8fAuf/Gvrf/xr63/8a+t//Fvrf/xb63/8W+t//Fvrf/1MzE/8e/t/8iJCb/BAkN/wkNEf8NERX/DQ0L/wICAf8PGiv/HTFN/x8wSf8bK0P/FyQ2/w8VH/8RFx//ERYe/wkQGP8OFB3/Exgf/xceJv8BChb/AAIO/zc8R/9HUF//OUNT/zU3PP88Mif/Rj00/0xHQv9LRUH/SkQ//0Q9OP9GQTz/aV1VgebVyixqa2oAAAAAAAAAAAAAAAAAAAAAAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDg1c3/083I/9jQy//b087/3NTP/9zV0P/c1dD/3NbQ/9zW0P/c1tD/3NbQ//338P+fm5j/AAAA/wQHC/8PEhX/Fhod/w4SFv8LDQ//CgkG/wAAAP8AAAD/BQUC/wQDAf8EBQT/BQcH/xMVFf8TFBT/CAkJ/xQVFv8AAAL/AwAA/4RzY//KtJ7/xrCb/8Kslv/KtKD/1MO0/9nKvf/bzL//2su+/9bFuP/Pva//1MO1/9XFuP/RwbP/f3NqgE5OTwBYWVkAWFlZAFhZWQD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////9/37/v/y8O7/7ejm/+nk4f/n4t//5+Lf/+fi3//n4t//5+Lf/+fi3///////h4WF/wAAAP8PExb/Fhkd/w8SFv8MDxP/Fxse/xEUF/8MDxP/GBsf/xoeIf8RFRj/FRgc/xEUGP8TFxr/ICMn/xgcH/8LEBX/AwYK/5qOg//56d3/2M/I/8/Gvv/Pxr7/1MvE/9vTzf/g2dT/4dvV/+Ha1f/b087/29TP/+zn5P/w7Or/19DL/8i2qP/16uJM//76AP/9+QD//fkA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AMC8t1n//Pn////////////08fD/7ern//Ds6v/v6+r/7+vq/+/s6v/v7Or//////5ybmv8AAAD/EhYa/w4SFf8OEhX/Gh0h/xUZHP8NEBP/GRwg/yElKP8YHB//DxMW/xkcIP8ZHCD/FBcb/xsfIv8iJSn/AAAC/01JRP/05dn/6OTh//Ht6//y7uz/6+bj/+nk4v/w6+n/9vLv//r18//18e//8Ovo//Tw7////v////////n39//38en/c2ZaswsEAAALBQAACwUAAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wADBAEA09DINMK+unfs5+Tn9fPz//Xy8f/39PP/+PX0//j19P/49fX/+PX0/////v/w7ez/ICMm/wIECP8UFxr/GBsf/xIVGf8KDhH/Fxoe/yUoK/8kKCv/ExYa/w8SFv8cHyP/HiIm/xodIf8YHB//HSEl/wAAA/+GfXb///71//n39/////////////v49//59fX//Pn5///8+v///////fr4//Tv7f///f7/////////////////9fLs/8i8sqOYk48AmJOQAJiTkAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8ANzYyANDHvQCnl4oA5N3a+v/////+/f3//v39//79/v/+/f7///7+//79/v/+/f7//////5OUlv8AAAD/FBgc/xEUGP8PEhX/Gh4h/ycrLv8rLjH/HiIl/w0QFP8TFxr/JSgr/yotMP8iJin/GRwg/xcbHv8AAAT/kYmD/////////////////////////f7/+/j3//jz8f/+/Pv//v39//Tx7//28/L///3+/////////////////93Syf/Cvbku5eTkAOXk5ADl5OQA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AKyimQC8rqQAyrqtF/Tu6v////////////////////////7///37+v////////////////+ho6b/AAAA/ycqLf8nKi3/Ki0w/zA0N/8yNDf/JSks/xQXGv8JDRD/HiEk/zY5PP80Njn/Ki0w/xodIf8UFxv/AAAE/2hkYP/////////////////+/P7//v7///7+/v/6+Pb/+vf3//n29f/6+Pf///////j18//z7en///n2//fv5t7Ev7lRAAABAAAAAAAAAAAAAAAAAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD6+PcA6+vrAOrp6QD07uqV/Pv7//////////////////r18uP49PB8///+/////v///v3/vrm35RcZHf8kKCv/LTAz/zs+QP8vMjX/HiEl/xEVGP8ICw7/ExYa/zk8Pv8/QUT/MjQ3/yEkJ/8SFhn/FRkd/xccIf8SFRj/1svC//////////////////////////////////7+/v/////////////////8+vr/7ufi/8G4sqjRy8UDsrGuAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A9O3mBO3h1p769vT/+vb0//Tt6dP69/Qx///+AMjDvy/i3dlp/v37XMK7tQgmKi94HyIl/yAjJv8kKCz/Ky4x/yMnKv8aHiD/HyEl/z5AQ/9JS07/MTM2/x8hJf8SFhn/EhUZ/x4iJf81Nzr/FRof/ywsLf/PysX///////////////////////n29f///////////////////////vz+//Do4v/07upG////APPy8ACLi4wAfX19AH19fQB9fX0A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////APPt5gDs2soA9e7nIfTv6inr4NcA/v/+AP///wCin5wA09HQAP///wCyragAHCInABofI2MtMDP9ISQn/ysuMv84Oj3/PD9C/0VHSv89P0H/Gx8i/w0QE/8WGh3/Gx4i/x8jJv8xNDf/PT9C/zw+Qf8OExj/EhMV/29tbf+ppJ7/mpKL/+be1/////////////////////////////37+//c0cnhYV9dBktLSwBMTU0AZmZlAGlpaQBpaWkAaWlpAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDz7eYA7d3OAPn07gD59/QA7ePbAP39/AD///8ArquoANjW1AD///8AtbCrAB4kKAAQFx0AICcsJisvM7YpLC7/ICMm/x4hJP8vMjX/IiUo/wUIC/8YGx//KSww/yUpLP8zNTn/QURH/z9CRP85PD7/PkFD/xkdIv8AAAD/AAAA/wAAAP8/Pj7/8u7q///////9+/r//Pv6//j18////vfdZ2NgIwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A8+3mAO3dzgD48+0A+PXyAO3j2wD9/fwA////AK6rqADY1tQA////ALWwqwAeJCgAExkfABwjKAAeJSoAJywxRCYpLa8eISTuIiUp4yMnK7kaHiLoNjk7/zY4O/8sLzL/PkBD/0RGSf8+QUP/PUBC/0RHSf9CREf/KCsu/xcaHv8eISX/AAAF3mBfXEjb19J+9/HsxPDq5cLw5t13///8BlFPTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////APPt5gDt3c4A+PPtAPj18gDt49sA/f38AP///wCuq6gA2NbUAP///wC1sKsAHiQoABMZHwAeJCkAHyUqACIoLgAlKjAAKS4zCyEmKwkaISUAJywwByktMV0rLjLqPT5B/0VHSv9HSk3/LTAz/yEkJ/83ODz/RUdJ/0ZIS/86PUDvLTA0nBAWHAo5Pj8AsaymAP///gD6+fgA9u3kAP///wBaWVcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDz7eYA7d3OAPjz7QD49fIA7ePbAP39/AD///8ArquoANjW1AD///8AtbCrAB4kKAATGR8AHiQpAB8lKgAkKS8AIygtACYrMAAkKS8AHCImACgtMQAiJywAGR8mES4yNa5KS07/UVJV/y4wM/8LDhL/GBwhryYqL14oLDJPIicrEB0iJwAMEhgASk5NAL25tAD///8A+/v6APXs4wD///8AW1lXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A8+3mAO3dzgD48+0A+PXyAO3j2wD9/fwA////AK6rqADY1tQA////ALWwqwAeJCgAExkfAB4kKQAfJSoAJCkvACMoLQAmKzAAJCkuABwiJgAnLDAAJSkuAB4kKwAZICUAKzA0fTw/Qt4tMDTWHSEmYBwiJwAeIykAICUsACAlKQAgJSkADRMZAEpOTQC9ubQA////APv6+QD17OMA////AFtZVwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////gB////////4AB////////AAD///////4AAH///////AAAP////wAAAAAf///8AAAAAAAB//wAAAAAAAH//AAAAAAAAf/8AAAAAAAB//4AAAAAAAH//wAAAAAAB//+AAAAAAAH//4AAAAAAA///wAAAAAA////AAAAAAB///+AAAAAAH///+IAAAAAf////wAAAAD/////gAAAAf////+AAAAB/////4AAAAD/////gAAAAP////+AAAAA/////4AAAAD/////gAAAAP////8AAAAA/////wAAAAD///7/AAAAAP//8AAAAAAA///wAAAAAAA///AAAAAAAB//8AAAAAAAD//wAAAAAAAP//gAAAAAAA///gAAAAAAD//8AAAAAAAf//4AAAAAAD///gQAAAAAf///n+AAAAB/////8AAAAP/////8AAAB//////8gAH////////gB/////////h/////////////////////////////////////////////////////////////////////////////////////////8='
        # Set up a minimize button
        self.minimize_button = ttk.Button(self.root, text="Minimize", command=self.minimize_to_tray)
        self.minimize_button.pack(pady=5)
        icon_data = base64.b64decode(icon_base64)
        icon_image = Image.open(BytesIO(icon_data))


        # Create the system tray icon with a specific menu
        self.icon = Icon("Screen Time Tracker", icon_image, menu=self.create_tray_menu())
        # Flag to track if the icon has been initialized
        self.icon_initialized = False

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        # GUI Components
        self.current_app_label = ttk.Label(self.root, text="Current App: None", font=("Arial", 14), background="#4a4a4a", foreground="white")
        self.current_app_label.pack(pady=10)

        self.total_time_label = ttk.Label(self.root, text="Total Screen Time: 0 mins", font=("Arial", 12), background="#4a4a4a", foreground="white")
        self.total_time_label.pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("App", "Total Time (mins)"), show="headings", height=15)
        self.tree.heading("App", text="App")
        self.tree.heading("Total Time (mins)", text="Total Time (mins)")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.export_button = ttk.Button(self.root, text="Export Log", command=self.export_log)
        self.export_button.pack(pady=5)
        self.view_button = ttk.Button(self.root, text="View Last Day's Data", command=self.view_last_day_data)
        self.view_button.pack(pady=5)
        # Data Structures
        self.current_app = None
        self.start_time = time.time()
        self.total_time_per_app = defaultdict(float)

        self.usage_sessions = defaultdict(list)

        self.switch_counter = 0  # Count app switches
        self.running = True
        self.schedule_periodic_save()

        # Start tracking in a background thread
        threading.Thread(target=self.track_screen_time, daemon=True).start()

    def format_duration(self, seconds):
        """Format duration into hours and minutes."""
        minutes = seconds // 60
        if minutes >= 60:
            hours = minutes // 60
            minutes %= 60
            return f"{int(hours)} hr {int(minutes)} min" if minutes else f"{int(hours)} hr"
        return f"{int(minutes)} min"

    def schedule_periodic_save(self):
        """Schedules the periodic save every 10 minutes (600,000 milliseconds)."""
        self.export_log()  # Initial save
        self.root.after(600000, self.schedule_periodic_save)  # Schedule next save in 10 minutes

    def minimize_to_tray(self):
        """Minimizes the window and places the icon in the system tray."""
        if not self.icon_initialized:
            # Start the tray icon only once
            self.tray_thread = threading.Thread(target=self.start_tray_icon, daemon=True)
            self.tray_thread.start()
            self.icon_initialized = True

        self.root.withdraw()  # Hide the main window
    def start_tray_icon(self):
        """Start the tray icon in a separate thread."""
        self.icon.run()

    def restore_window(self, icon, item):
        """Restores the main window from the system tray."""
        self.root.deiconify()  # Show the main window
    def quit_application(self, icon, item):
        """Closes the application completely."""
        self.export_log()  # Export data before quitting
        icon.stop()  # Stop the system tray icon
        self.root.quit()  # Quit Tkinter application
    def wnd_proc(self, hwnd, msg, wparam, lparam):
        """Handles Windows messages to detect system shutdown."""
        if msg == win32gui.WM_QUERYENDSESSION:
            # Trigger export before shutdown
            self.export_log()
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def create_tray_menu(self):
        """Creates the tray menu with options: Open to restore window, Quit to close the app."""
        return Menu(
            MenuItem("Open", self.restore_window),
            MenuItem("Quit", self.quit_application)
        )


    def get_active_window_exe(self):
        """Fetch the executable name of the currently active window."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return "Unknown"
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name().replace('.exe', '')  # Remove .exe from the name
        except Exception:
            return "Unknown"

    def track_screen_time(self):
        """Tracks screen time for each application in the background."""
        while self.running:
            active_app = self.get_active_window_exe()

            if active_app != self.current_app:
                if self.current_app:
                    # Log session details for the previous app
                    end_time = time.time()
                    duration = end_time - self.start_time
                    self.total_time_per_app[self.current_app] += duration
                    self.usage_sessions[self.current_app].append({
                        "start": datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S"),
                        "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"),
                        "duration": duration
                    })
                    self.switch_counter += 1  # Increment switch counter

                # Update current app
                self.current_app = active_app
                self.start_time = time.time()

                # Update GUI
                self.update_gui()

            time.sleep(1)

    def update_gui(self):
        """Updates the GUI with the latest data."""

        # Update current app
        self.current_app_label.config(text=f"Current App: {self.current_app}")

        # Update total screen time
        total_time = sum(self.total_time_per_app.values())
        self.total_time_label.config(text=f"Total Screen Time: {self.format_duration(total_time)}")

        # Update treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        for app, time_spent in self.total_time_per_app.items():
            self.tree.insert("", "end", values=(app, self.format_duration(time_spent)))

    def export_log(self):
        """Exports the usage log to a CSV file with the date in the filename."""
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{today}.csv"
        combined_sessions = self.combine_sessions()

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Application", "Start Time", "End Time", "Duration (seconds)", "Duration (Formatted)"])

            for session in combined_sessions:
                writer.writerow([
                    session["app"],
                    session["start"],
                    session["end"],
                    round(session["duration"], 2),
                    self.format_duration(session["duration"])
                ])
        print(f"Log exported to {file_name}")
    def combine_sessions(self):
        """Combine overlapping or consecutive sessions into a unified log."""
        combined = []

        for app, sessions in self.usage_sessions.items():
            if not sessions:
                continue

            # Sort sessions by start time
            sessions = sorted(sessions, key=lambda x: datetime.strptime(x["start"], "%Y-%m-%d %H:%M:%S"))
            merged = [sessions[0]]

            for current in sessions[1:]:
                last = merged[-1]
                last_end = datetime.strptime(last["end"], "%Y-%m-%d %H:%M:%S")
                current_start = datetime.strptime(current["start"], "%Y-%m-%d %H:%M:%S")

                # If sessions overlap or are consecutive, merge them
                if current_start <= last_end:
                    last["end"] = max(last["end"], current["end"])
                    last["duration"] += current["duration"]
                else:
                    merged.append(current)

            # Add merged sessions for this app
            for session in merged:
                session["app"] = app
                combined.append(session)

        return combined

    def load_previous_day_data(self):
        """Load the previous day's data if available, but do not mix it with today's data."""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{yesterday}.csv"
        print(file_name)
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    app, start, end, duration, duration_min = row
                    # Convert to appropriate types and append to usage_sessions for viewing only
                    duration = float(duration)
                    if app not in self.usage_sessions:
                        self.usage_sessions[app] = []
                    self.usage_sessions[app].append({
                        "start": start,
                        "end": end,
                        "duration": duration
                    })
            print(f"Loaded previous day's data from {file_name}")

    def stop_tracking(self):
        """Stops the tracking loop, exports the data, and exits the application."""
        self.running = False
        self.export_log()  # Export data when the app is closed
        self.root.destroy()  # Close the application

    def view_last_day_data(self):
        """Opens a new window to view the last day's screen time data."""
        # Load the previous day's data
        self.load_previous_day_data()

        # Create a new top-level window
        preview_window = Toplevel(self.root)
        preview_window.title("Last Day's Screen Time Data")

        # Get screen width and height to center the window
        screen_width = preview_window.winfo_screenwidth()
        screen_height = preview_window.winfo_screenheight()
        window_width = 800
        window_height = 750
        # Calculate position for centering the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        preview_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        preview_window.config(bg="#4a4a4a")  # Set background color for preview window

        # Add a treeview to show the data
        tree = ttk.Treeview(preview_window, columns=("App", "Total Time (mins)"), show="headings", height=10)
        tree.heading("App", text="App")
        tree.heading("Total Time (mins)", text="Total Time (mins)")
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Aggregate and sort apps by usage time
        sorted_apps = sorted(self.total_time_per_app.items(), key=lambda x: x[1], reverse=True)

        # Limit the CSV to show the top 10 entries
        for app, time_spent in sorted_apps[:10]:
            tree.insert("", "end", values=(
                app,
                round(time_spent / 60, 2)
            ))

        # Generate the chart
        self.create_usage_chart(sorted_apps[:10], preview_window)

        # Display switch count summary
        switch_label = ttk.Label(preview_window, text=f"Total App Switches: {self.switch_counter}", font=("Arial", 14),
                                 background="#4a4a4a", foreground="white")
        switch_label.pack(pady=10)

    def load_previous_day_data(self):
        """Load the previous day's data if available, but do not mix it with today's data."""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{yesterday}.csv"
        print(file_name)
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    app, start, end, duration, duration_min = row
                    # Convert to appropriate types and append to usage_sessions for viewing only
                    duration = float(duration)
                    if app not in self.total_time_per_app:
                        self.total_time_per_app[app] = 0
                    self.total_time_per_app[app] += duration

                    if app not in self.usage_sessions:
                        self.usage_sessions[app] = []
                    self.usage_sessions[app].append({
                        "start": start,
                        "end": end,
                        "duration": duration
                    })
            print(f"Loaded previous day's data from {file_name}")

    def create_usage_chart(self, sorted_apps, preview_window):
        """Generates a bar chart for the app usage with apps on the Y-axis."""
        apps = [app for app, _ in sorted_apps]
        times = [time_spent / 60 for _, time_spent in sorted_apps]  # Convert to minutes

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#4a4a4a')  # Set light gray background for the figure

        # Bar chart with apps on the Y-axis
        ax.barh(apps, times, color='#4a4a4a')
        ax.set_ylabel('Application')
        ax.set_xlabel('Time (Minutes)')
        ax.set_title("App Usage for Last Day", color="white")

        # Set text color to white for chart labels
        ax.tick_params(axis='both', colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

        # Save the chart to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Convert image to Tkinter compatible format and display
        img = Image.open(buf)
        img = img.resize((600, 400), Image.Resampling.LANCZOS)  # Adjust the size as needed
        chart_image = ImageTk.PhotoImage(img)

        # Add the chart image to the window
        chart_label = ttk.Label(preview_window, image=chart_image)
        chart_label.image = chart_image
        chart_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTimeTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.minimize_to_tray)  # Minimize window to tray on close
    root.mainloop()