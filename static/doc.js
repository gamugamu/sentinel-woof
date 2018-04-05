Vue.component('step', {
  props: ['title', 'method', 'url_root', 'route', 'use', 'curl_cmd', 'data', 'm_return'],
  template: `
    <div>
      </br>
      <h5>• {{title}}</h5>
      <p><i>{{use}}</i></p>
      <b class="grey darken-3 white-text method">{{method}}</b> {{url_root}}<b class="cyan lighten-5">{{route}}</b></route>
      <table class="bordered">
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
      <b>Return</b>
      <div class="return">
        <i><p>{{m_return}}</p></i>
      </div>
    </div>
  `,computed: {
    // un accesseur (getter) calculé
    curl_command: function () {
      // `this` pointe sur l'instance vm
      var cmd = "curl -i -H \"Content-Type: application/json\" -X " + this.method + " -d '{";

      for(var key in this.curl_cmd){
        console.log("---> ", key, this.$parent._data[key]);
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
      cmd += "}' " + this.url_root + this.route;
      return cmd
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
          console.log("****");
          sessionStorage.setItem("auth_login", val)
        }
    }
});
