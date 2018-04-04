Vue.component('step', {
  props: ['title', 'method', 'url_root', 'route', 'use', 'bash_cmd', 'data', 'm_return', 'client_id', 'provider'],
  template: `
    <div>
      </br>
      <h5>{{title}}</h5>
      <p><i>{{use}}</i></p>
      <b class="black white-text">{{method}}</b> {{url_root}}<b class="grey lighten-2">{{route}}</b></route>
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
      <pre><code class="language-bash line-numbers">curl -i -d '{\"client_id\" : "{{client_id}}",  {{bash_cmd}} -H &quot;Content-Type: application/json&quot; -X {{method}} {{url_root}}{{route}}}</code></pre>
      <b>Return</b>
      <div class="grey lighten-2">
        <i><p>{{m_return}}</p></i>
      </div>
    </div>
  `
})

//var bsh_me_auth = "\"provider\";:&quot;google&quot;, &quot;token&quot;:&quot;xxx&quot;}''"

var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data:{
    client_id: sessionStorage.getItem("client_id")
  },
  watch: {
        'client_id': function(val, oldVal){
          console.log("called");
          sessionStorage.setItem("client_id", val)
        },
        'provider': function(val, oldVal){
        console.log("p called");
        sessionStorage.setItem("provider", val)
        }
    }
});
