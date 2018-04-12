
Vue.component('step', {
  props: ['title', 'method', 'url_root', 'route', 'required_bearer', 'use', 'curl_cmd', 'data', 'm_return', 'return_id'],
  template: `
    <div>
      <h5 v-if="title">• {{title}}</h5>
      <h5 v-else></br></h5>
      <b class="orange darken-3 white-text method">{{method}}</b> {{url_root}}<b class="cyan lighten-5">{{route}}</b></route>
      <p><i>{{use}}</i></p>
      <table class="bordered" v-if="this.data != undefined">
       <thead>
         <tr>
             <th><i>key</i></th>
             <th><i>value</i></th>
         </tr>
       </thead>
       <tbody>
       <tr v-for="(v, k) in data">
          <th>{{k}}</th>
          <td>{{v}}</td>
       </tr>
       </tbody>
       </table>
      <pre><code class="language-bash line-numbers">{{curl_command}}</code></pre>
      <button v-on:click="call_curl_cmd()">test it</button>
      <b>Return</b>
          <pre class="return margin_tight">
            {{json_return}}
          </pre>
    </div>
  `,computed: {
    // un accesseur (getter) calculé
    curl_command: {
      get: function () {
      // `this` pointe sur l'instance vm
      var cmd = "curl -i -H \"Content-Type: application/json\" "
      if (this.required_bearer == "true"){
          cmd += '-i -H "Authorization: Bearer XXXX_TOKEN_XXXX "'
      }

      if (this.curl_cmd != undefined){
        cmd += "-X " + this.method + " -d '{"

        for(var key in this.curl_cmd){
          var value = this.curl_cmd[key]

          if ( value.charAt(0) == '*' ) {
            k = value.substr(1, value.lenght);
            v = typeof this.$parent._data[k] !== 'undefined' ? this.$parent._data[k] : ""

            cmd += "\"" + key + "\":" + "\"" + v +  "\", "
          }else{
            cmd += "\"" + key + "\":" + "\"" + value +  "\", "
          }
        }
        cmd = cmd.slice(0, -2); // ', '
        cmd += "}' "
      }
      //var obj                   = JSON.parse(this.m_return);
      //ciResponseText.innerHTML  = JSON.stringify(obj, undefined, 2);
      var obj = JSON.parse(this.m_return);
      obj     = JSON.stringify(obj, undefined, 2);
      console.log(obj);
      this.json_return = "\n" + obj
    //  console.log("stringyfied ---> ", obj);

      cmd += this.url_root + this.route;

      return cmd
      }
    }
  },
  methods: {
    call_curl_cmd: function(cmd){
      console.log("will parse ", this.curl_command);
      var res = parse_curl_js.parse(`curl 'http://127.0.0.1:8000/'`);
      console.log(JSON.stringify(res, null, 2));
      console.log("done");
    // const curlCmd = `curl 'http://server.com:5050/a/c/getName/?param1=pradeep&param2=kumar&param3=sharma'`;
  }
}
})

var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data:{
    client_id: sessionStorage.getItem("client_id"),
    provider: sessionStorage.getItem("provider"),
    auth_login: sessionStorage.getItem("auth_login"),
  },
  watch: {
        'client_id': function(val, oldVal){
          sessionStorage.setItem("client_id", val)
        },
        'provider': function(val, oldVal){
          sessionStorage.setItem("provider", val)
        },
        'auth_login': function(val, oldVal){
          sessionStorage.setItem("auth_login", val)
        }
    }
});
