

function test(box,x){
  
 var element;
   
  
  for(var i=0;i<=3;i++){

    element = document.getElementById("r"+i);
    element.style.fill="";
  }
   element = document.getElementById("r"+x);
   if(element.style.fill==="orange"){
    element.style.fill="";
    }
    else{
      element.style.fill="orange";
    }
  //  document.getElementById("st").value=document.getElementById("stime").value;
  //  document.getElementById("et").value=document.getElementById("etime").value;
    document.getElementById("slotselected").value=x;

}
function al(){
    alert("Please log in.");
}

 function validate(stat){
    if((document.getElementById('st').value=="") || (document.getElementById('et').value=="") ||(document.getElementById("slotselected").value=="") || (document.getElementById('dst').value=="") 
    || (document.getElementById('det').value=="") ){
        alert("Enter Start time and End time");
        return false
    }
    if(stat){
        return true;
    }
    else{
        alert("Please login or sign up.");
        return false;
    }
 }

const resetdate = function() {
var d = new Date();
  document.getElementById("stime").defaultValue = d.getHours()+":"+d.getMinutes();
  document.getElementById('st').value = document.getElementById('stime').value;
  document.getElementById('et').value = document.getElementById('etime').value;

};

const gridpoll = function(){
    //var catid;
    //catid = $(this).attr("data-catid");
    $.ajax(
    {
        type:"GET",
        url: "/grid/grid/",
        dataType : 'json',
          data:{
                 status:"true",
        }, 
        
        success: function( data ) 
        {
          
            for(var i=0;i<=3;i++){
              element = document.getElementById("r"+i);
                if (data[i]==1){
                  console.log(data[i]);
                  element.classList.add("redrect");
                  element.classList.remove("greenrect");
                }
                else{
                  console.log("two");
                  element.classList.add("greenrect");
                  element.classList.remove("redrect");
                }
          }
          console.log(data[0]);
           console.log(typeof data);
           console.log(data);
        }
     })
};




function closeScanner(scanner){
  //scanner.stop()
  $("#scanModal").hide();
}

function scannerCallback(content){
        console.log(content);
        var qrReq=new XMLHttpRequest;
        XMLHttpRequest.responseType="json";
        qrReq.onload = function(){
          scanner.stop();
          var res=JSON.parse(this.response);
          var status = parseInt(res["status"])
          var message = "internal error"
          if(status == 1){
            message = "Reservation Done"
          }
          else if(status == 2){
            message = "Please book a seat before scanning"
          }
          else if(status == 3){
            message = "Already reserved"
          }
          else if(status == 4){
            message = "Vehicle is not detected, you have to park the vehicle before scanning"
          }
          else if(status == -1){
            message = "Please log in to confirm reservation"
          }
          document.getElementById("booking_alert").style.display="inline-block";
          document.getElementById("message").innerHTML=message;
          closeScanner(scanner);
        }
      var data=JSON.stringify({"slot_id":content});
      qrReq.open("post", "/grid/scan/", true);
      qrReq.setRequestHeader("Content-Type", "application/json");
      qrReq.send(data);
      }
// function qrScanner(scanner){
//       scanner.addListener('active', );
//       Instascan.Camera.getCameras().then(function (cameras) {
//         if (cameras.length > 0) {
//           scanner.start(cameras[0]);
//         } else {
//           console.error('No cameras found.');
//         }
//       }).catch(function (e) {
//         $("scanModal").hide()
//         console.error(e);
//       });
// }

function closeAlertBox(){
  document.getElementById("booking_alert").style.display="none";
  document.getElementById("message").innerHTML="";
}

