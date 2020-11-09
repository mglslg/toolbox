import requests


def post_risk_online(url, cookie_str):
    # Cookie中的内容直接将浏览器中的值复制下来即可！
    headers = {
        'User-Agent': 'self-defind-user-agent',
        'Cookie': cookie_str
    }
    proxies = {
        'http': 'http://suolongga:Slg5295793@proxy.soydai.me:8080',
        'https': 'http://suolongga:Slg5295793@proxy.soydai.me:8080'
    }
    response = requests.post(url, headers=headers, proxies=proxies)
    return response


def post_risk_nrc(url, cookie_str):
    # Cookie中的内容直接将浏览器中的值复制下来即可！
    headers = {
        'User-Agent': 'self-defind-user-agent',
        'Cookie': cookie_str
    }
    proxies = {
        'http': 'http://nrc.proxy.soydai.me:8888',
        'https': 'http://nrc.proxy.soydai.me:8888'
    }
    response = requests.post(url, headers=headers, proxies=proxies)
    return response


if __name__ == '__main__':
    url = 'https://admin.souyidai.com/afterloan/pageform/json/category/list'
    cookie = 'smidV2=20201016091356f7d59bcf4026a8f2dea8b2a3ce2798470012fb525f5badba0; u_main=fa6482c693d19d89c27911aaeddb7a4e; u_after-loan_admin_souyidai_com=d1090e6d010e9a38a70e987c8111b7cd; u_risk_admin_souyidai_com=48f2f75148e7f488bca8f545170570b3; Hm_lvt_51bfa68f6bea432417d90d76280e520f=1603950473; Hm_lpvt_51bfa68f6bea432417d90d76280e520f=1603953169; JSESSIONID=D3F8CF5CCD47EEB2B1B4C7AD47B87E83; u_fyd_admin_souyidai_com=d0b07fbd8acc33d0b68247b291d684a0; auth_info=c3VvbG9uZ2dhfDE2MDQ1NjUxMzM1Mzk=; auth_hash=956ddcc82ae90d01431249f8fa5100b9'
    rs = post_risk_online(url, cookie)
    print(rs.text)
