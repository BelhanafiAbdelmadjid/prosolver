import login from "@/views/login.vue"
import supervision from "@/views/supervision.vue"

import incidentList from "@/views/incidents/index.vue"
import incidentCreate from "@/views/incidents/create.vue"
import incidentShow from "@/views/incidents/show.vue"
import incidentEdit from "@/views/incidents/edit.vue"
import incidentExecute from "@/views/incidents/execute.vue"

import stepCreate from "@/views/steps/create.vue"
import stepShow from "@/views/steps/show.vue"
import stepEdit from "@/views/steps/edit.vue"

import serverList from "@/views/servers/index.vue"
import serverCreate from "@/views/servers/create.vue"
import serverShow from "@/views/servers/show.vue"
import serverEdit from "@/views/servers/edit.vue"

import scriptList from "@/views/scripts/index.vue"
import scriptCreate  from "@/views/scripts/create.vue"
import scriptShow  from "@/views/scripts/show.vue"
import scriptEdit  from "@/views/scripts/edit.vue"

import users from "@/views/users-inetrraction.vue"

import page404 from "@/views/page_404.vue"


const routes = [
  {path: '/',redirect: '/Login' },
  {path: '/Login' , component : login , name:"login" ,meta : { hideNav : true } },
  { path: '/supervision', component: supervision ,name:"supervision"},
  
  { path: '/incidents', component: incidentList ,name:"incidentsList"},
  { path: '/incidents/create', component: incidentCreate ,name:"incidentCreate"},
  { path: '/incidents/:id', component: incidentShow ,name:"incidentShow" , props : true},
  { path: '/incidents/:id/execute', component: incidentExecute ,name:"incidentExecute" , props : true},
  { path: '/incidents/:id/edit', component: incidentEdit ,name:"incidentEdit" , props : true},
  
  { path: '/incidents/:id/steps/create', component: stepCreate ,name:"stepCreate" , props : true},
  { path: '/incidents/:id/steps/:stepID', component: stepShow ,name:"stepShow" , props : true},
  { path: '/incidents/:id/steps/:stepID/edit', component: stepEdit ,name:"stepEdit" , props : true},
  
  { path: '/servers', component: serverList ,name:"serverList"},
  { path: '/servers/create', component: serverCreate ,name:"serverCreate"},
  { path: '/servers/:id', component: serverShow ,name:"serverShow"},
  { path: '/servers/:id/edit', component: serverEdit ,name:"serverEdit"},
  
  { path: '/scripts', component: scriptList ,name:"scriptList"},
  { path: '/scripts/create', component: scriptCreate ,name:"scriptCreate"},
  { path: '/scripts/:id', component: scriptShow ,name:"scriptShow"},
  { path: '/scripts/:id/edit', component: scriptEdit ,name:"scriptEdit"},
  
  { path: '/users', component: users ,name:"users"},
  
  {path: "/:catchAll(.*)",name: "NotFound",component : page404,meta : { hideNav : true }}
]

export default routes