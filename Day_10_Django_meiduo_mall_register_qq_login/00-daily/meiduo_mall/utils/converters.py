class UsernameConverter:
    """自定义路由转换器去匹配用户名"""
    # 定义匹配用户名的正则表达式
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return str(value)


class MobileConverter:
    regex = r'1[3-9]\d{9}'

    def to_python(self, value):
        return value
