import sys
import time
import win32gui
import win32process
import psutil
import threading
import pandas as pd
import ctypes
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, Toplevel, PhotoImage
from collections import defaultdict
import csv
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import io
import base64
from pystray import Icon, MenuItem, Menu

