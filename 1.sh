set_var() {
    API="https://api.telegram.org/bot5581975233:AAH0IItRrom_bA_Qp7AvrKx2nFgPNJYpoXI"
    GID="chat_id=-905471380"
    MSG="${API}/sendMessage?${GID}&text="
    SF="${API}/sendDocument?${GID} -F document=@"
    script_name=$(basename "$0")
    ecr_dr_pre='asia-southeast1-docker.pkg.dev/disaster-recovery-408903/up'
    ecr_pre='126738739392.dkr.ecr.ap-southeast-1.amazonaws.com'
    ecr_uat='126738739392.dkr.ecr.ap-southeast-1.amazonaws.com'
    ecr_test='934891041601.dkr.ecr.ap-southeast-1.amazonaws.com'
    env=$(pwd | awk -F'/' '{print $5}')
    service=$(basename "${0%.sh}")
    rm -f build.sh .gitignore
    rm -rf .git risk activity admin api asset assistant auth betting data gambling guessing java-gateway java-wallet java-portal java-admin k8s-build mongo notify payment redistest report rfc search statics tweet uas user wallet ws web 
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

check_file_extension() {
    # 检查文件名是否以 .sh 结尾
    if [[ "$script_name" != *.sh ]]; then
        send_message "当前文件名必须以 .sh 后缀结尾"
        exit 1
    fi
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

git_clone() {
    # Clone 代码
    if [ "$env" == "test"    ] ; then bran=test ;fi
    if [ "$env" == "pre"     ] ; then bran=pre  ;fi
    if [ "$env" == "dr-pre"  ] ; then bran=pre  ;fi
    if [ "$env" == "uat"     ] ; then bran=main ;fi

    if [ "$service" == "up-backend-activity-service"  ] ; then app='activity'        ; git_dir='activity'         ;fi
    if [ "$service" == "up-backend-admin-service"     ] ; then app='admin'           ; git_dir='admin'            ;fi
    if [ "$service" == "up-backend-api-service"       ] ; then app='api'             ; git_dir='api'              ;fi 
    if [ "$service" == "up-backend-asset-service"     ] ; then app='asset'           ; git_dir='asset'            ;fi
    if [ "$service" == "up-backend-assistant-service" ] ; then app='assistant'       ; git_dir='assistant'        ;fi
    if [ "$service" == "up-backend-auth-service"      ] ; then app='auth'            ; git_dir='auth'             ;fi
    if [ "$service" == "up-backend-betting-service"   ] ; then app='betting'         ; git_dir='betting'          ;fi
    if [ "$service" == "up-backend-data-service"      ] ; then app='data'            ; git_dir='data'             ;fi
    if [ "$service" == "up-backend-gambling-service"  ] ; then app='gambling'        ; git_dir='gambling'         ;fi
    if [ "$service" == "up-backend-guessing-service"  ] ; then app='guessing'        ; git_dir='guessing'         ;fi
    if [ "$service" == "up-backend-notify-service"    ] ; then app='notify'          ; git_dir='notify'           ;fi
    if [ "$service" == "up-backend-payment-service"   ] ; then app='payment'         ; git_dir='payment'          ;fi
    if [ "$service" == "up-backend-report-service"    ] ; then app='report'          ; git_dir='report'           ;fi
    if [ "$service" == "up-backend-rfc-service"       ] ; then app='rfc'             ; git_dir='rfc'              ;fi
    if [ "$service" == "up-backend-search-service"    ] ; then app='search'          ; git_dir='search'           ;fi
    if [ "$service" == "up-backend-statics-service"   ] ; then app='statics'         ; git_dir='statics'          ;fi
    if [ "$service" == "up-backend-tweet-service"     ] ; then app='tweet'           ; git_dir='tweet'            ;fi
    if [ "$service" == "up-backend-uas-service"       ] ; then app='uas'             ; git_dir='uas'              ;fi
    if [ "$service" == "up-backend-user-service"      ] ; then app='user'            ; git_dir='user'             ;fi
    if [ "$service" == "up-backend-wallet-service"    ] ; then app='wallet'          ; git_dir='wallet'           ;fi
    if [ "$service" == "up-backend-ws-service"        ] ; then app='ws'              ; git_dir='ws'               ;fi
    if [ "$service" == "up-backend-risk-service"      ] ; then app='risk'            ; git_dir='risk'             ;fi

    if [ "$service" == "up-web-2upgame-ingress"       ] ; then app='web-2upgame'     ; git_dir='web/2upgame-vn'   ;fi
    if [ "$service" == "up-web-admin-ingress"         ] ; then app='web-admin'       ; git_dir='web/admin'        ;fi
    if [ "$service" == "up-web-agent-h5-ingress"      ] ; then app='web-agent-h5'    ; git_dir='web/agent-h5'     ;fi
    if [ "$service" == "up-web-bti-ingress"           ] ; then app='web-bti'         ; git_dir='web/bti'          ;fi
    if [ "$service" == "up-web-h5-ingress"            ] ; then app='web-h5'          ; git_dir='web/2up-h5'       ;fi 
    if [ "$service" == "up-web-license-ingress"       ] ; then app='web-license'     ; git_dir='web/license'      ;fi  

    if [ "$service" == "java-backend-gateway-service" ] ; then app='java-gateway'     ; git_dir='java-gateway'    ;fi
    if [ "$service" == "java-backend-wallet-service"  ] ; then app='java-wallet'      ; git_dir='java-wallet'     ;fi
    if [ "$service" == "java-backend-portal-service"  ] ; then app='java-portal'      ; git_dir='java-portal'     ;fi
    if [ "$service" == "java-backend-admin-service"   ] ; then app='java-admin'       ; git_dir='java-admin'      ;fi 
    if [ "$service" == "java-backend-rank-service"    ] ; then app='java-rank'        ; git_dir='java-rank'       ;fi

    git init
    git config --global init.defaultBranch $bran
    git remote add origin http://2upcid:c3idBdo4fed2@gitlab.2up.one/devops/deploy.git
    git config core.sparsecheckout true
    echo "$git_dir/*" > .git/info/sparse-checkout
    git config --global --add safe.directory .
    git pull origin $bran 
    commit_id=$(git log -1 | grep commit | awk '{print $2}')
    echo "当前函数 $FUNCNAME 当前环境 $env 拉取代码分支 $bran 当前业务模块 $app 当前代码路径 $git_dir 当前commit_id $commit_id"
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

build_docker_image() {
    # 构建 Docker 镜像
    curl -s $MSG"$env+环境开始构建项目镜像+$service" > /dev/null
    echo "当前函数 $FUNCNAME 当前镜像 $service:$commit_id"
    docker build --no-cache -t "$service:$commit_id" . || {
        send_message "构建镜像++$service:$commit_id++失败++ok++@Vyser0369++@Ben_Bird++@qqqer12"
        exit 1
    }
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

push_docker_image() {
    # 推送 Docker 镜像到容器仓库
    if [ "$env" == "test"    ] ; then ecr=$ecr_test ;fi
    if [ "$env" == "pre"     ] ; then ecr=$ecr_pre  ;fi
    if [ "$env" == "dr-pre"  ] ; then ecr=$ecr_dr_pre  ;fi
    if [ "$env" == "uat"     ] ; then ecr=$ecr_uat ;fi

    echo "当前函数 $FUNCNAME 当前环境 $env 当前仓库 $ecr"

    docker tag "$service:$commit_id" "$ecr/$service:$commit_id"
    # 判断 $env 不同环境推送不同仓库
    if [[ "test dev" =~ $env ]]; then
        export AWS_PROFILE=test
        aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin $ecr > /dev/null
        docker push "$ecr/$service:$commit_id" > /dev/null
        curl -s $MSG"$env+推送镜像++$ecr/$service:$commit_id++测试仓库成功++ok" > /dev/null
    fi

    if [[ "pre uat" =~ $env ]]; then
        export AWS_PROFILE=prod
        aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin $ecr > /dev/null
        docker push "$ecr/$service:$commit_id" > /dev/null
        curl -s $MSG"$env+推送镜像++$ecr/$service:$commit_id+++线上仓库成功++ok" > /dev/null
    fi

    if [[ "dr-pre" =~ $env ]]; then
        image_push_json
        gcloud auth activate-service-account --key-file='image-push.json' > /dev/null
        docker login -u _json_key -p "$(cat image-push.json)" https://gcr.io > /dev/null
        docker push "$ecr/$service:$commit_id" > /dev/null
        curl -s $MSG"$env+推送镜像++$ecr/$service:$commit_id+++谷歌仓库成功++ok" > /dev/null
    fi

    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

update_helm_chart() {
    # 更新 Helm Chart 版本
    echo "当前函数 $FUNCNAME 当前环境 $env 当前Helm分支 $env"   
    git clone -b $env http://2upcid:c3idBdo4fed2@gitlab.2up.one/2upcid/HelmChart.git
    nu=`cat -n HelmChart/$service/values.yaml | grep '  tag: ' | awk '{print $1}'`
    sed -i "${nu}s/.*/  tag: $commit_id/" HelmChart/$service/values.yaml
    cd HelmChart/
    git add "$service/values.yaml"
    git -c user.email="uatelop@2box.me" -c user.name="2upcid" commit -m "Modify line 11 and add tag $commit_id"
    git push origin $env
    cd ..
    rm -rf HelmChart
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

deploy_to_env() {
    # 部署到 env 环境
    # 判断 $env 部署到不同环境
    if [[ "test dev" =~ $env ]]; then
    echo "当前函数 $FUNCNAME 当前环境 $env 当前argo地址 argodev.2upops.com 当前argo服务 $env-$service" 
    argocd login argodev.2upops.com --username admin --password pWwQFtJVyYjMSGv3 
    sleep 3
    argocd app sync "$env-$service" 
    sleep 10
    HealthyNumber=`argocd app get "$env-$service" |grep Healthy | wc -l`
        if [ "$HealthyNumber" -ge 1 ]; then 
            curl -s $MSG"镜像++$service:$commit_id++部署到+$env+环境成功++ok" > /dev/null
        else 
            curl -s $MSG"镜像++$service:$commit_id++部署到+$env+环境失败++@UNedme" > /dev/null
        fi
    argocd logout > /dev/null
    fi

    if [[ "pre uat dr-pre" =~ $env ]]; then
    echo "当前函数 $FUNCNAME 当前环境 $env 当前argo地址 argocd.2upuat.com 当前argo服务 $env-$service" 
    argocd login argocd.2upuat.com  --username admin --password tL7MqJXdFzp5n52p 
    sleep 3
    argocd app sync "$env-$service" 
    sleep 10
    HealthyNumber=`argocd app get "$env-$service" |grep Healthy | wc -l`
        if [ "$HealthyNumber" -ge 1 ]; then
            curl -s $MSG"镜像++$service:$commit_id++部署到+$env+环境成功++ok" > /dev/null
        else 
            curl -s $MSG"镜像++$service:$commit_id++部署到+$env+环境失败++@UNedme" > /dev/null
        fi
    argocd logout > /dev/null
    fi
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

image_push_json() {
cat > image-push.json << EOF
{
    "type": "service_account",
    "project_id": "disaster-recovery-408903",
    "private_key_id": "3d62ef10a798e91aa28ad518a7d721d1065585dc",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCu/SxplUi5covh\nc5mIM/B26ZCjzUhuQ0LD50y90o1RRuSAvURZzFCvX2OEkWTcufepi1JY4cK5CAen\n28tJOP8TuyhpJwfSMMT7mB4poKFyFc05rew/pUoU/ETAb5BxU0KahBLSCYSPd8iY\nnogtO9fgEzTBe901hlby+BlXFnQpYAooYpR7+GiLIwuJLHB25WSVIqIO/9QI2z/e\nHltr4ApkA/QeVydvBYW4sLv08om2XV/gW22LEEhLs+wmW6IKgB/IH68kZ+vvjidt\n9SS8nRt41Eu9qo2tBQR3Clu3ZVEj/vHGugs8tLkpBpjME8p3BTrFsfhzvHw3JO/o\nKLUTnOXrAgMBAAECggEANsFb01H2Jqk0IgDFKvxtoxfkvYyvvGjpjFllBwTKWYNg\nXvRaXerz2Fx1zHaeY/8BAxloVA2Ym8Nqedjp3GisUGVA+N5QsTG3ga6QyZ/MxOET\njZfhk+zJqJVjgf+m5/8QmT74kKaPx0DJERCSNe1C2IfJ+z0h8+ysamy9qSWKhaNW\nEYPsluhH5GYwzo2Vo269AAoP+XLA4AojHLckl2lFM63e1ZLhBYSIsOnsGqKHWU33\nUefqglFZczeThWwR9Dn/tG9tayP1K8jvnw2MWFghk9V3JAYN3idwU1r2qgzYwUzJ\nSKG7pwjyCs+P5UBoPoSuxSbX54WjJHbgVqkrJgDS6QKBgQDdlVJDGMFh7yrKLNdY\nWtATlvIWzIj3QbunFcqWu+txj+uLxs7ryRehzgakPIgSZ5A/NsToLWfo6+Iy3+FY\nIib2OhP2RBWBzHGZsAwaKpi6XfNGlhmsMQ1y2harNg9DT10Kg8lrtF1wv8FmKGOo\nU2XypJGRz9nArHZBjA42VbWBbwKBgQDKKyaculOj/kbPyeIRhKc391kNi0JddfSN\nOX/0yr8yfTJN9WpD2308eCUuHxKYN22bs6v2ZsKNrmC52X0uIMZE82kWog/S0JtB\nrgRDTzYzvYBl2JFRrwiNi8iO/8zv7kEfqCs0c5+PxSqmI7P1qUWb3v5bjNv4f2Jv\nH7oMs9etRQKBgA1WlLoXPmTPycqbwma+KLJVLsNykngXy9z18dj6/OQ8HpiuYfxN\ngY+q4Dl4r1Q0SbmUaWv0d8HMmTQox97PR3sg6dy0IntKvDfdIg1dLQ5i42cHWApG\ndaHJQP4TZf3ORDKC1lgWZl2IHXMx0TXrt0JQ57ZYRapUd1XgwWZB6IgfAoGBAKw5\ncl1VxecQuRZOr42o6iMdTfnhxpmD4N9mOoE5LwQ971rGVM6V7uxSlaniwp51qaRY\nvYfdJqQ4ByKMCr3/Iaifi8jCKqS3HWwoaG1Gz6/oIbehdLqXV7vtdt+LPvSujUAA\nrT2zuhxqJNj/1VDT8P7GSv2G0+Wv7xUnfAFSO8vZAoGBAKNeKqtcpY3Xrn9ENMNL\nJx/fTg8VA3wuNPgA6DvPbd/icYSjYgd2Qvzd8GQQGpChasqp77PxFOXGAy/8D6XX\nTeZawg2diJoGfpQsoug4oX6U6w1ZU6Bo2KbRyKlll/nFvdG3p2ATixDpPWHYMeOp\nIx+ajg1YgiJ4MsugMUh83mfd
-----END PRIVATE KEY-----
",
    "client_email": "image-push@disaster-recovery-408903.iam.gserviceaccount.com",
    "client_id": "116501333511336758995",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/image-push%40disaster-recovery-408903.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
EOF
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

clean_docker_images() {
    # 清理 Docker 镜像
    docker rmi "$service:$commit_id" "$ecr/$service:$commit_id" > /dev/null
    rm -rf .git "$app" web > /dev/null
    rm -f image-push.json > /dev/null
    rm -f build.sh .gitignore
    rm -rf .git risk activity admin api asset assistant auth betting data gambling guessing java-gateway java-wallet java-portal java-admin k8s-build mongo notify payment redistest report rfc search statics tweet uas user wallet ws web 
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}

main() {
    set_var               #设置环境变量检查脚本
    check_file_extension
    git_clone
    build_docker_image 
    push_docker_image     #更新helm的tag
    update_helm_chart 
    deploy_to_env         #部署模块到k8s环境 
    clean_docker_images 
    local result=$? ; echo "函数 $FUNCNAME 执行后返回 $result" ; return "$result"
}
main