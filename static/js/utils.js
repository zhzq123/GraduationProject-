String.prototype.endWith = function (str) {
    if (str == null || str == "" || this.length == 0 || str.length > this.length) {
        return false;
    }
    if (this.substr(this.length - str.length, str.length) == str) {
        return true;
    } else {
        return false;
    }
};

function check_email(email) {
    if (!email.endWith('@minieye.cc'))
        return '邮箱格式不符'
    if (email.length > 30) {
        return '邮箱太长'
    }
    return true
}

function check_psw(psw) {
    if (psw.length > 25 || psw.length < 4) {
        return '密码长度应在4到25之间'
    }
    let level = 0
    for (index in psw) {
        let item = (psw[index])
        if (item >= 'a' && item <= 'z') {
            level |= 1
        } else if (item >= 'A' && item <= 'Z') {
            level |= 2
        } else if (item >= '0' && item <= '9') {
            level |= 4
        } else {
            level |= 8
        }
    }
    if ((level - 1) & level) {
        return true
    } else {
        return '密码应该至少包括大写字母，小写字母，数字，其余符号四种中的两种'
    }
}