      var buttID;
      var levelAID;
      var onloadCallback = function() {
        buttID = grecaptcha.render('butt',{'sitekey' : 'XXXXXXXXXX',
          'callback' : letIn1});
        levelAID = grecaptcha.render('levelA',{'sitekey' : 'XXXXXXXXXX',
          'callback' : letInA});
      }
      function validate(event){
        event.preventDefault();
        grecaptcha.execute();
      }
      function showElem(id) {
        document.getElementById(id).style.display = "initial";
      }
      function hideElem(id) {
        document.getElementById(id).style.display = "none";
      }
      function hideButtons() {
        hideElem("buttonContainer");
      }
      function processName(inputName){
        var name = null;
        var processedName = null;
        var numberCheck = /[0-9]/g;
        var gmaCheck = /gma/g;
        try{
          name = inputName;
          processedName = name.trim().toLowerCase();
        }catch(e){
          //console.warning(e);
        }
        if (numberCheck.test(processedName) || gmaCheck.test(processedName)){
          name = "false";
          return name;
        }
        else {
          return name;
        }
      }
      function letInA(token){
        var name = null;
        var checkedName = null;
        try{
          name = prompt('Enter name to alert Slack OR press OK to skip');
          checkedName = processName(name);
        }catch(e){
          console.warning(e);
        }
        if (checkedName === ""){
          letIn('aLevel');
        }
        else if(checkedName == null){
          alert('Your request has been canceled');
        }
        else if(checkedName === "false"){
          hideButtons();
          showElem("ligmaStatus");
        }
        else if(checkedName != "" && checkedName != null){
          postSlack(name,'aLevel');
        }
      }
      function letIn1(token){
        var name = null;
        var checkedName = null;
        try{
          name = prompt('Enter name to alert Slack OR press OK to skip');
          checkedName = processName(name);
        }catch(e){
          console.warning(e);
        }
        if(checkedName === ""){
          letIn('1Level');
        }
        else if(checkedName == null){
          alert('Your request has been canceled');
        }
        else if(checkedName === "false"){
          hideButtons();
          showElem("ligmaStatus");
        }
        else if(checkedName != "" && checkedName != null){
          postSlack(name,'1Level');
        }
      }
      function letIn(level) {
        showElem("waitingStatus");
        hideButtons();
        var response;
        var responseButt = grecaptcha.getResponse(buttID);
        var responseLevelA = grecaptcha.getResponse(levelAID);
        if(responseButt == null || responseButt === ""){
          response = responseLevelA;
        }
        else {
          response = responseButt;
        }

        var params = {
          level: level,
          response: response
        };

        var json = JSON.stringify(params);

        fetch(`/activate`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: json})
          .then(resp => {
            if (resp.ok) {
                hideElem("waitingStatus");
                return resp.text().then(text => {
                    if (text === "timeout") {
                        showElem("timedOutStatus");
                    } else if (text === "buttonpressed") {
                        showElem("comingStatus");
                    }
                });
            }
        })
      }
      function postSlack(name, level){
        if(level ==="aLevel"){
          levelString = "Level A";
        }
        else if(level === "1Level"){
          levelString = "Level 1"
        }
        var params = {
          "text":`<!here> ${name} wants to get in from ${levelString}`
        }
        fetch('XXXXXXXXXXXXXXXXXXXXXXX',
          {method: 'POST', body: JSON.stringify(params)})
          .then(() => letIn(level))
          .catch((error) => console.log(error));
      }