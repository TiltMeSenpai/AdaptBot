var instance = null

export default class Api {
  constructor() {
    if(!instance){
          instance = this;
    }
    return instance;
  }

  setSession(session){
    this.session = session
  }

  setSecret(secret){
    this.key = secret
  }

  request(method, url, data = {}) {
    return new Promise(function(resolve, reject){
      var xhr = new XMLHttpRequest()
      xhr.open(method, url)
      xhr.responseType = "json"
      xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
          resolve(xhr.response)
        }else if (xhr.readyState == 4) {
          reject(new Error("Status error: "+xhr.status))
        }
      }
      xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
      xhr.setRequestHeader('Authorization', this.session)
      var payload = JSON.stringify(data)
      var hash = CryptoJS.HmacSHA256(payload, this.key).toString(CryptoJS.enc.Hex)
      xhr.send(JSON.stringify({'data': payload, 'signature': hash}))
    }.bind(this))
  }
}
