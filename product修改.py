@product.route('/one-password')
def obtain_one_password():
    code = request.args.get('code')
    if code:
        app_token = create_app_token()
        user_token = create_user_token(app_token, code)
        user_info = get_user_info(app_token, user_token)
        apply_mail = user_info.get("apply_mail")
        user = OnePasswdModel.query.filter_by(apply_mail=apply_mail).first()
        if apply_mail:
            if user.status == USER_STATUS:
                q = request.args.get('q')
                data = decrypt_data(zlib.decompress(base64.b64decode(q)), SECRET)
                device_info = dict(urlparse.parse_qsl(urlparse.urlsplit(data).path))
                pass_info = get_one_password(device_info)
                passwd = pass_info.get('passwd')
                lc_num = pass_info.get('lc_num')
                return render_template('/product/one-password.html', passwd=passwd, lc_num=lc_num)
            else:
                return render_template('/product/one-password-error.html', message="用户不一致")
        else:
            return render_template('/product/one-password-error.html', message="无email")
    else:
        return render_template('/product/one-password-error.html', message="code无效")


def query_user(lc_no, apply_mail, auth_style, start_time, end_time, operator):
    user = OnePasswdModel()
    user.certificate_no = lc_no
    user.apply_mail = apply_mail
    user.start_time = start_time
    user.end_time = end_time
    user.apply_time = datetime.datetime.now()
    user.operator = operator
    user.authorize = auth_style

    return user


@login_required
@one_password.route('/authorization', methods=['POST'])
def apply_authorization():
    """
        lc_no :证书编号
        apply_mail: 申请人邮箱
        operator: 操作人
        auth_style: 临时授权 or永久授权
    :return:
    """

    data = request.form.to_dict()
    lc_no = data.get("lc_no")
    apply_mail = data.get("apply_mail")
    auth_style = data.get("auth_style")
    operator = data.get("operator")

    if not all([lc_no, apply_mail, auth_style, operator]):
        return jsonify({"status": 400,"message": "参数不完整"})
    if auth_style == SHORT_TIME_NUM:
        auth_style = SHORT_TIME_NUM
        start_time = datetime.datetime.now()
        end_time = start_time + timedelta(hours=4)
    else:
        auth_style = LONG_TIME_NUM
        start_time = datetime.datetime.now()
        end_time = start_time + timedelta(days=10000)

    user = query_user(lc_no, apply_mail, auth_style, start_time, end_time, operator)
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": 201, "message": "资源创建成功"})


@login_required
@one_password.route('/qrcode')
def one_passwd_qrcode():
    """
        生成一次性密码的二维码
    :return:
    """
    certificate_no = request.args.get("lc_no")
    serial = request.args.get("serial")
    if not all([certificate_no, serial]):
        return jsonify({"status": 400,"message": "参数不完整"})
    user = OnePasswdModel.query.filter_by(certificate_no=certificate_no).first()
    if  not user:
        return jsonify({"status": 400,"message": "请求错误"})
    user.serial=serial
    db.session.commit()
    qrcode = None
    if user and user.status == USER_STATUS:
        from ..util.device_code import DeviceCode
        image = DeviceCode()
        qrcode = image.make()
        print (qrcode)
        return jsonify({"status":200,"message":"请求成功","qrcode": qrcode,})
    else:
        return jsonify({"status": 403,"message": "用户没有权限"})


@login_required
@one_password.route('/records')
def one_passwd_records():
    """
        一次性密码申请记录部分
    :return:
    """
    apply_mail = request.args.get("apply_mail")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_num", 5))

    if not apply_mail:
        return jsonify({"status": 400,"message": "参数不完整"})

    users = OnePasswdModel.query.filter_by(apply_mail=apply_mail).limit(page_size).offset((page - 1) * page_size)

    data_list = []
    if users:
        for user in users:
            data = {}
            data["lc_no"] = user.certificate_no
            data["serial"] = user.serial
            data["apply_mail"] = user.apply_mail
            data["authorize"] = user.authorize
            data["status"] = user.status
            data["apply_time"] = user.apply_time
            data["confirm_time"] = user.confirm_time
            data_list.append(data)

        context = {
            "status": 200,
            "message":"申请成功",
            "data": data_list,
        }
        return jsonify(**context)

    else:
        return jsonify({"status": 404,"message": "无法找到请求资源"})

