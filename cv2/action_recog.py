import sys, cv2
from scipy import spatial
import cv2, time, logging
import os
import torch
import numpy as np
import importlib
from cab_action.gesture.gesture_recog import object_detect

# PATH_ROOT = "/home/byb/test_envs/cab_action_recognize.log"
# logger = logging.getLogger('action_recog')
# logger.setLevel(level=logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s  - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# file_handler = logging.FileHandler(PATH_ROOT)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

"""
ActionRecog:recognize the action and get the action frame list from rstp
"""


class ActionRecog():
    def __init__(self, config_path="config"):
        # 载入模型
        cfg = importlib.import_module(config_path)
        self.gesture_model = object_detect(**cfg.gesture_classifier_parma)
        # print(self.gesture_model.names)
        self.which_hand_index = 0  # 判断做动作手臂的帧
        self.frame = []  # 缓存图像数据
        self.ges_list = []  # 缓存手势列表
        self.analysis_dict = {}  # 返回字典
        self.analysis_dict["hand_frame_center"] = [0, 0]
        self.analysis_dict["template"] = 0

    def gesture_predict(self, frame):
        """
        手势预测
        frame: 输入图像
        return: 
        result_frame: 带标注信息的图像
        pred: [x1,y1,x2,y2,cls]的集合
        """
        result_frame, pred, names = self.gesture_model.recongnize(frame)
        return result_frame, pred

    def compute_iou(self, rec1, rec2):
        """
        计算 IoU
        :param rec1: (y0, x0, y1, x1), which reflects
                (top, left, bottom, right)
        :param rec2: (y0, x0, y1, x1)
        :return: scala value of IoU
        """
        # computing area of each rectangles
        S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

        # computing the sum_area
        sum_area = S_rec1 + S_rec2

        # find the each edge of intersect rectangle
        left_line = max(rec1[1], rec2[1])
        right_line = min(rec1[3], rec2[3])
        top_line = max(rec1[0], rec2[0])
        bottom_line = min(rec1[2], rec2[2])

        # judge if there is an intersect
        if left_line >= right_line or top_line >= bottom_line:
            return 0
        else:
            intersect = (right_line - left_line) * (bottom_line - top_line)
            return (intersect / (sum_area - intersect)) * 1.0

    def action_predict(self, frame, human_state):
        """
        计算输入的每一帧图像,根据缓存判断是否发生动作,并输出分析字典
        frame: 输入图像
        human_state: True = sit  False = stand
        return: 
        flag: 1 检测到动作   0 没有检测到动作
        finger_num:
        analysis_dict: template_index,analysis_frame_list,center
        """
        # 当队列超过100时,推出队头
        if len(self.ges_list) > 100:
            self.ges_list.pop(0)
            self.frame.pop(0)
        # 保存当前帧
        save_frame = cv2.resize(frame, (360, 640))
        self.frame.append(save_frame)
        # 预测手势
        result_frame, pred = self.gesture_predict(frame)
        # print(pred)

        if human_state:
            # 更新坐姿缓存手势列表
            if len(pred) == 0:
                self.ges_list.append(0)
            else:
                pred_ = np.array(pred)
                cls_ = pred_[:, 4]
                conf_ = pred_[:, 5]
                if len(cls_[cls_ == 0]) == 1:
                    # print(pred)
                    self.ges_list.append(1)
                    if len(pred) == 2 and conf_[cls_ == 0][0] > 0.6 and self.analysis_dict["hand_frame_center"][0] != 0:
                        if self.compute_iou(pred_[0, :4], pred_[1, :4]) < 0.1:
                            if len(pred_[cls_ == 0]) != 0:
                                key = pred_[cls_ == 0]
                            else:
                                key = pred_[cls_ == 1]
                            self.analysis_dict["hand_frame_center"] = [int((key[0][0] + key[0][2]) / 2),
                                                                       int((key[0][1] + key[0][3]) / 2)]
                            self.analysis_dict["hand_frame"] = save_frame
                elif len(cls_[cls_ == 1]) == 1 and conf_[cls_ == 1][0] > 0.6:
                    # print(pred)
                    self.ges_list.append(1)
                # elif len(cls_[cls_== 6]) > 0 and conf_[cls_==6][0] > 0.65:
                #     self.ges_list.append(-1)

                else:
                    self.ges_list.append(0)

            # if len(self.ges_list) >= 16:
            if len(self.ges_list) >= 40:
                ges_feat = np.array(self.ges_list)
                # if sum(ges_feat) > 0 and sum(ges_feat[-6:]) == 0:
                if sum(ges_feat) > 0 and sum(ges_feat[-25:]) == 0:
                    # print("ananlysis the action list")
                    self.select_analysis_list(human_state)
                    self.analysis_dict["finger_num"] = sum(ges_feat)
                    return 1, self.analysis_dict
            # print("enter last frame")
            return 0, {}
        else:
            # 更新站姿缓存手势列表
            if len(pred) == 0:
                self.ges_list.append(0)
            else:
                pred_ = np.array(pred)
                cls_ = pred_[:, 4]
                conf_ = pred_[:, 5]
                # print(pred)
                if len(cls_[cls_ == 0]) == 1:
                    self.ges_list.append(1)
                    if len(pred) == 2 and conf_[cls_ == 0][0] > 0.6 and self.analysis_dict["hand_frame_center"] != 0:
                        if self.compute_iou(pred_[0, :4], pred_[1, :4]) == 0:
                            if len(pred_[cls_ == 0]) != 0:
                                key = pred_[cls_ == 0]
                            else:
                                key = pred_[cls_ == 1]
                            self.analysis_dict["hand_frame_center"] = [int((key[0][0] + key[0][2]) / 2),
                                                                       int((key[0][1] + key[0][3]) / 2)]
                            self.analysis_dict["hand_frame"] = save_frame
                elif len(cls_[cls_ == 1]) == 1:
                    self.ges_list.append(1)
                elif len(cls_[cls_ == 6]) > 0 and conf_[cls_ == 6][0] > 0.65:
                    self.ges_list.append(-1)
                else:
                    self.ges_list.append(0)

            ges_feat = np.array(self.ges_list)
            if len(self.ges_list) >= 60:
                if sum(ges_feat[:-1]) > 0 and ges_feat[-1] == -1:
                    self.select_analysis_list(human_state)
                    self.analysis_dict["finger_num"] = sum(ges_feat[:-1])
                    # print("ananlysis the action list")
                    return 1, self.analysis_dict
            elif len(self.ges_list) <= 30 and ges_feat[-1] == -1:
                self.ges_list = []
            # print("enter last frame")
            return 0, {}

    def select_analysis_list(self, human_state):
        """
        根据缓存输出分析字典
        human_state: True = sit  False = stand
        return: 
        analysis_dict: which_hand_index,analysis_frame_list
        从100帧图像里面挑选符合的图像帧
        """
        first_finger_index = self.ges_list.index(1)
        # 
        if human_state:
            for i in range(2, len(self.ges_list) + 1):
                if self.ges_list[len(self.ges_list) - i] == 1:
                    self.which_hand_index = len(self.ges_list) - i
                    break
            if first_finger_index > 25:
                analysis_list = [first_finger_index - 20, self.which_hand_index + 20]
            elif first_finger_index <= 25 and first_finger_index > 10:
                analysis_list = [first_finger_index - 10, self.which_hand_index + 20]
            else:
                analysis_list = [first_finger_index, self.which_hand_index + 20]

        else:
            for i in range(2, len(self.ges_list) + 1):
                if self.ges_list[len(self.ges_list) - i] == 1:
                    self.which_hand_index = len(self.ges_list) - i
                    break
            analysis_list = [0, len(self.ges_list)]

        analysis_frame = []
        count = 1
        self.analysis_dict["template"] = count
        analysis_frame.append(self.frame[analysis_list[0]])
        for j in range(analysis_list[0] + 1, analysis_list[1]):
            if j == self.which_hand_index:
                self.analysis_dict["template"] = count
            if j % 3 == 0:
                count += 1
                analysis_frame.append(self.frame[j])
            elif j % 3 != 0 and self.ges_list[j] == 1:
                count += 1
                analysis_frame.append(self.frame[j])
            else:
                continue
        self.analysis_dict["frame"] = analysis_frame
        self.analysis_dict["finger_num"] = 0
        # self.analysis_dict["save_frame"] = self.frame

        # 清缓存
        if human_state:
            for k in range(self.which_hand_index + 1):
                self.ges_list.pop(0)
                self.frame.pop(0)
        else:
            self.ges_list.clear()
            self.frame.clear()

    def _clear(self):
        self.ges_list.clear()
        self.frame.clear()
        self.analysis_dict = {}
        self.analysis_dict["hand_frame_center"] = [0, 0]
