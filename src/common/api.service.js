import toolKit from "@/main.js"
export default class apiFetch{
    
    static BASE_URL = "http://192.168.1.52:5000/api";
    static get(endpoint,emit,throwErr){
        if(throwErr == null){
            throwErr = false;
        }
        return new Promise((resolve,reject)=>{
            fetch(this.BASE_URL+endpoint,{
                method: "GET",
                credentials: "include", 
                headers: { 
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            })
            .then((response)=>{
                console.log(response.headers)
                if(response.status == 401){
                    toolKit.router.push('/login')
                }else if(response.status == 403){
                    toolKit.router.back()
                    
                }
                response.json()
                .then((data)=>{
                    if(emit){
                        console.log("response",response.ok)
                        toolKit.emitter.emit("sidebar-error",{
                            error : !response.ok,
                            description : data.msg
                        })
                    }
                    if(response.ok){
                        resolve(data);
                    }else if(throwErr == true && !response.ok){
                        reject(data);

                    }
                })
                
            })
            .catch((err)=>{
                console.log(err);
            })
        })
    }
    static post(endpoint,payload,emit,throwError){
        return new Promise((resolve,reject)=>{
            fetch(this.BASE_URL+endpoint,{
                method: "POST",
                credentials: "include", 
                headers: { 
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({ 
                    ...payload
                  })
            })
            .then((response)=>{
                console.log(response.headers)
                response.json()
                .then((data)=>{
                    if(response.status == 401){
                        toolKit.router.push('/login')
                    }
                    if(response.ok){
                        resolve(data);
                    }else{
                        // toolKit.router.go()
                        if(throwError){
                            reject(data);
                        }
                    }
                    if(emit){
                        toolKit.emitter.emit("sidebar-error",{
                            error : !response.ok,
                            description : data.msg
                        })
                    }
                })
                
            })
            .catch((err)=>{
                console.log(err)
            })
        })

    }
    static update(endpoint,payload,emit,throwError){
        return new Promise((resolve,reject)=>{
            fetch(this.BASE_URL+endpoint,{
                method: "PUT",
                credentials: "include", 
                headers: { 
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({ 
                    ...payload
                  })
            })
            .then((response)=>{
                response.json()
                .then((data)=>{
                    if(response.status == 401){
                        toolKit.router.push('/login')
                    }
                    if(response.ok){
                        resolve(data);
                    }else{
                        toolKit.router.go()
                        if(throwError){
                            reject(data);
                        }
                    }
                    if(emit){
                        toolKit.emitter.emit("sidebar-error",{
                            error : !response.ok,
                            description : data.msg
                        })
                    }
                })
                
            })
            .catch((err)=>{
                console.log(err)
            })
        })

    }
    static delete(endpoint,payload,emit,throwError){
        return new Promise((resolve,reject)=>{
            fetch(this.BASE_URL+endpoint,{
                method: "DELETE",
                credentials: "include", 
                headers: { 
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({ 
                    ...payload
                  })
            })
            .then((response)=>{
                response.json()
                .then((data)=>{
                    if(response.status == 401){
                        toolKit.router.push('/login')
                    }
                    if(response.ok){
                        resolve(data);
                    }else{
                        // toolKit.router.go()
                        if(throwError){
                            reject(data);
                        }
                    }
                    if(emit){
                        toolKit.emitter.emit("sidebar-error",{
                            error : !response.ok,
                            description : data.msg
                        })
                    }
                })
                
            })
            .catch((err)=>{
                console.log(err)
            })
        })

    }
}

// export default class apiFetch{
//     static BASE_URL = "http://192.168.1.56:5000/api";
//     static get(endpoint,emit,throwErr){
//         if(throwErr == null){
//             throwErr = false;
//         }
//         return new Promise((resolve,reject)=>{
//             fetch(this.BASE_URL+endpoint,{
//                 method: "GET",
//                 credentials: "include", 
//                 headers: {
//                     "Content-Type": "application/json",
//                 }
//             })
//             .then((response)=>{
//                 console.log(response.headers)
//                 if(response.status == 401){
//                     toolKit.router.push('/login')
//                 }
//                 response.json()
//                 .then((data)=>{
//                     if(emit){
//                         toolKit.emitter.emit("sidebar-error",{
//                             error : response.ok,
//                             description : data.msg
//                         })
//                     }
//                     if(response.ok){
//                         resolve(data);
//                     }else if(throwErr == true && !response.ok){
//                         reject(data);
//                     }
//                 })
                
//             })
//             .catch((err)=>{
//                 console.log(err);
//             })
//         })
//     }
//     static post(endpoint,payload,emit,throwError){
//         return new Promise((resolve,reject)=>{
//             fetch(this.BASE_URL+endpoint,{
//                 method: "POST",
//                 credentials: "include", 
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body : JSON.stringify({ 
//                     ...payload
//                   })
//             })
//             .then((response)=>{
//                 console.log(response.headers)
//                 response.json()
//                 .then((data)=>{
//                     if(response.status == 401){
//                         toolKit.router.push('/login')
//                     }
//                     if(response.ok){
//                         resolve(data);
//                     }else{
//                         if(throwError){
//                             reject(data);
//                         }
//                     }
//                     if(emit){
//                         toolKit.emitter.emit("sidebar-error",{
//                             error : !response.ok,
//                             description : data.msg
//                         })
//                     }
//                 })
                
//             })
//             .catch((err)=>{
//                 console.log(err)
//             })
//         })

//     }
//     static update(endpoint,payload,emit,throwError){
//         return new Promise((resolve,reject)=>{
//             fetch(this.BASE_URL+endpoint,{
//                 method: "PUT",
//                 credentials: "include", 
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body : JSON.stringify({ 
//                     ...payload
//                   })
//             })
//             .then((response)=>{
//                 response.json()
//                 .then((data)=>{
//                     if(response.status == 401){
//                         toolKit.router.push('/login')
//                     }
//                     if(response.ok){
//                         resolve(data);
//                     }else{
//                         if(throwError){
//                             reject(data);
//                         }
//                     }
//                     if(emit){
//                         toolKit.emitter.emit("sidebar-error",{
//                             error : !response.ok,
//                             description : data.msg
//                         })
//                     }
//                 })
                
//             })
//             .catch((err)=>{
//                 console.log(err)
//             })
//         })

//     }
//     static delete(endpoint,payload,emit,throwError){
//         return new Promise((resolve,reject)=>{
//             fetch(this.BASE_URL+endpoint,{
//                 method: "DELETE",
//                 credentials: "include", 
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body : JSON.stringify({ 
//                     ...payload
//                   })
//             })
//             .then((response)=>{
//                 response.json()
//                 .then((data)=>{
//                     if(response.status == 401){
//                         toolKit.router.push('/login')
//                     }
//                     if(response.ok){
//                         resolve(data);
//                     }else{
//                         if(throwError){
//                             reject(data);
//                         }
//                     }
//                     if(emit){
//                         toolKit.emitter.emit("sidebar-error",{
//                             error : !response.ok,
//                             description : data.msg
//                         })
//                     }
//                 })
                
//             })
//             .catch((err)=>{
//                 console.log(err)
//             })
//         })

//     }
// }



// toolKit.router.beforeEach((to) => {
//     if(to == "supervision" && toolKit.router.query.UAT == null && toolKit.router.query.Prod == null){
//         toolKit.router.query.UAT = true;
//     }
//     return false
//   })