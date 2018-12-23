from define.Const import TYPE_LOGIN_NORMAL_WAY, TYPE_LOGIN_OTHER_WAY
from define.UrlsConf import loginUrls
from net.NetUtils import EasyHttp
from utils.Log import Log
from train.login import recognize


class Captcha(object):
    __REPONSE_NORMAL_CDOE_SUCCESSFUL = '4'
    __REPONSE_OHTER_CDOE_SUCCESSFUL = '1'

    def getCaptcha(self, type=TYPE_LOGIN_NORMAL_WAY):
        urlInfo = loginUrls['other']['captcha'] if type == TYPE_LOGIN_OTHER_WAY else loginUrls['normal']['captcha']
        Log.v('正在获取验证码..')
        return EasyHttp.send(urlInfo)

    def check(self, results, type=TYPE_LOGIN_NORMAL_WAY):
        if type == TYPE_LOGIN_OTHER_WAY:
            return self._checkRandCodeAnsyn(results)
        return self._captchaCheck(results)

    def _checkRandCodeAnsyn(self, results):
        formData = {
            'randCode': results,
            'rand': 'sjrand',
        }
        jsonRet = EasyHttp.send(loginUrls['other']['captchaCheck'], data=formData)
        print('checkRandCodeAnsyn: %s' %jsonRet)

        def verify(response):
            return response['status'] and Captcha.__REPONSE_OHTER_CDOE_SUCCESSFUL == response['data']['result']

        return verify(jsonRet)

    def _captchaCheck(self, results):
        data = {
            'answer': results,
            'login_site': 'E',
            'rand': 'sjrand',
        }
        result = EasyHttp.send(loginUrls['normal']['captchaCheck'], data=data)
        Log.v('验证码校验结果：%s'%result.get('result_message'))

        return result.get('result_code') == '4'


    def verifyCaptchaByHand(self, type=TYPE_LOGIN_NORMAL_WAY):
        code_base64 = self.getCaptcha(type)
        results = recognize.auto_recognize(code_base64)
        return results, self.check(results, type)


if __name__ == '__main__':
    pass

