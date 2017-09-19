#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class weibo:
    def __init__(self, usr_id, usr_pw):
        self.driver = webdriver.Chrome()
        self.usr_id = usr_id
        self.usr_pw = usr_pw

        self.posts_to_be_deleted = 99999
        # save status
        self.logged = False

        # wait for browser pop out
        time.sleep(5)

    def login(self):
        if self.logged:
            return
        """login start from sina.com.cn.
        It would be very chaotic if you direticly go to weibo.com when you are abroad.
        """
        self.driver.get('https://login.sina.com.cn/signup/signin.php')
        login_id_xpath = '//*[@id="username"]'
        login_pw_xpath = '//*[@id="password"]'
        login_button_xpath = '//*[@id="vForm"]/div[2]/div/ul/li[7]/div[1]/input'
        login_id = self.driver.find_element_by_xpath(login_id_xpath)
        login_pw = self.driver.find_element_by_xpath(login_pw_xpath)
        login_button = self.driver.find_element_by_xpath(login_button_xpath)
        login_id.send_keys(self.usr_id)
        login_pw.send_keys(self.usr_pw)
        login_button.click()
        time.sleep(5)

        # then go to weibo.com
        self.driver.get('https://www.weibo.com')
        time.sleep(5)
        self.logged = True

    def go_to_post(self):
        my_posts_button_xpath = '//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/ul/li[3]/a/strong'
        my_posts_button = self.driver.find_element_by_xpath(my_posts_button_xpath)
        my_posts_button.click()
        time.sleep(5)

    def del_lastest_post(self):
        posts_arrow_xpath = '//*[@class="screen_box"]/a'
        posts_arrow = self.driver.find_element_by_xpath(posts_arrow_xpath)
        posts_arrow.click()
        time.sleep(1)

        del_button = self.driver.find_element_by_link_text('删除')
        del_button.click()

        self.confirm();

    def del_posts(self):
        num_post = self.posts_to_be_deleted
        if num_post < 0:
            n_try = 99999
            print("all posts will be deleted!")
        else:
            n_try = num_post
            print("{} posts will be deleted.".format(n_try))

        self.login()
        self.go_to_post()
        posts_xpath = '//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[3]/a/strong'
        posts = self.driver.find_element_by_xpath(posts_xpath)
        origin = int(posts.text)
        print("before deleting", posts.text)

        i_go = 0
        while(i_go < origin):
            time.sleep(1)
            try:
                if i_go % 10 == 0 and i_go > 0:
                    print("{} has been deleted".format(i_go))
                del_me()
                i_go += 1
            except:
                print("failed, try again.")

        self.refresh()
        posts = self.driver.find_element_by_xpath(posts_xpath)
        print("total posts left", posts.text)

    def confirm(self):
        time.sleep(0.5)
        confirm_page = self.driver.switch_to_active_element()
        confirm_page.send_keys(Keys.ENTER)

    def refresh(self):
        time.sleep(1)
        self.driver.refresh()
        time.sleep(10)

    def unfollow_latest(self):
        ls_btn_xpath = '//*[@id="Pl_Official_RelationMyfollow__93"]/div/div/div/div[3]/ul/li[1]/div[1]/div[2]/div[5]/p/a[2]/em'
        ls_btn = self.driver.find_element_by_xpath(ls_btn_xpath)
        #ls_btn = self.driver.find_element_by_link_text('E')
        ls_btn.click()

        unfollow_button = self.driver.find_element_by_link_text('取消关注')
        unfollow_button.click()

        self.confirm()

    def unfollow(self):
        self.login()
        self.go_to_post()

        follow_button_xpath = '//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[1]/a/strong'
        follow_button = self.driver.find_element_by_xpath(follow_button_xpath)
        total_follow = int(follow_button.text)
        print("total following:", total_follow)
        follow_button.click()

        i_go = 0
        i_try = 0
        while i_go < total_follow and i_try < 0.5*total_follow:
            time.sleep(2)
            try:
                if i_go % 15 == 0 and i_go > 0:
                    print("{} are unfollowed".format(i_go))
                    self.refresh()
                self.unfollow_latest()
                i_go += 1
            except:
                i_try += 1
                print("failed, try again")

        self.refresh()
        follow_number_xpath = '//*[@id="Pl_Official_RelationLeftNav__81"]/div[2]/div[1]/div/div/div/div/ul/li[1]/a/em[2]'
        follow_number = self.driver.find_element_by_xpath(follow_number_xpath)
        current_follow = int(follow_number.text)
        print("after unfollowing", current_follow)

if __name__ == "__main__":
    usr_id = 'xxxx@gmail.com'
    usr_pw = 'xxxx'
    am_i = weibo(usr_id, usr_pw)
    am_i.unfollow()
