<template>
    <table class="tg">
        <tr>
            <th class="tg-cly1">
                <div class="line"></div>
            </th>
            <th class="tg-cly1">
                <div class="line"></div>
            </th>
            <th class="tg-cly1">
                <div class="line"></div>
            </th>
        </tr>
        <tr>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
        </tr>
        <tr>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
        </tr>
        <tr>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
        </tr>
        <tr>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
            <td class="tg-cly1">
                <div class="line"></div>
            </td>
        </tr>
    </table>
</template>
<script>
</script>
<style scoped>

  


.container{
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.tg{
   border-collapse:collapse;
   border-spacing:0;
   border-color:#ccc;

   height: 25px;
}
.tg td{
  font-family:Arial, sans-serif;
  font-size:14px;padding:10px 5px;
  border-style:solid;
  border-width:0px;
  overflow:hidden;
  word-break:normal;
  border-color:#ccc;
  color:#333;
  background-color:#fff;

  height: 25px;
}
.tg th{
  font-family:Arial, sans-serif;
  font-size:14px;
  font-weight:normal;
  padding:10px 5px;
  border-style:solid;
  border-width:0px;
  overflow:hidden;
  word-break:normal;
  border-color:#ccc;
  color:#333;
  background-color:#f0f0f0;

  height: 25px;
  
}

.line{
    float: left;
    width: 100px;
    height: 16px;
    margin-top: 12px;
    border-radius: 7px;
    
    background-image: linear-gradient(90deg, #F4F4F4 0px, rgba(229,229,229,0.8) 40px, #F4F4F4 80px);
    background-size: 600px;
    animation: shine-lines 2.0s infinite ease-out;
}

 
@keyframes shine-lines{
    0% { background-position: -100px;}
    40%, 100% {background-position: 140px;}
}


</style>