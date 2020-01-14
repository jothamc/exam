var json_data;
var unanswered = []
var unansweredOptions = {}

function newQuestion(number,option){
    //Generates HTML for a new question
    var template = $("<div class='question-container' id='"+number+"'>")
    var heading = $("<div class='question'>").append($("<h5>").text("Question "+number))
    heading.append($("<img class='img-fluid' src='/media/"+number+".jpg' alt='"+number+"'>"))
    template.append(heading)
    template.append(newOption(number,option))
    return template
}

function newOption(number,option){
    //Generates HTML for new option in a question
    var container = $("<div class='options'>")
    container.append($("<label>").text("Option "+option.toUpperCase()))
    container.append($("<img class='img-fluid' src='/media/"+number+option+".jpg' alt='"+number+option+"'>"))
    var content = $("<div class='option input-group'>")
    content.append($("<div class='input-group-prepend'>").append($("<span class='input-group-text'>").text("Enter A or D")))
    content.append($("<input type='text' class='form-control answer' name='"+number+"-"+option+"' required>"))
    container.append(content)
    return container
}

function changeOption(number,option) {
    newOption(number,option).insertAfter($("div.options").last())
}

var checkInputAnswer = function(event){
    //Queries backend for answer of an input
    input = $(this);
    val = input.val().toUpperCase()
    if (val != "A" && val != "D" ){
        input.val("")
    } else {
        input.val(val)
        $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            url:$("form#questions-form")[0].action,
            type:"POST",
            data:input.serialize(),
            success:function(data){
                alert(data.answer)
                params = input.serializeArray()[0]
                num_option = params.name.split("-")
                num = num_option[0]
                option = num_option[1]
                if (askQ(num,option) == false) askQ()
            }
        })
    }
}

$.ajax({
    //Runs on page load to retrieve questions
    headers: { "X-CSRFToken": csrf_token },
    url: modeURL,
    type:"POST",
    data:{"start":1},
    success:function(data){
        if(data){
            json_data = data
            unanswered = json_data.question_keys
            askQ()
        }
    }
})



function askQ(number=undefined,option=undefined){
    //Displays new question.
    //Returns false if last option in question has been displayed
    //Returns true if options are remaining in question
    if(number != undefined){
        number = parseInt(number)
        var j = unansweredOptions[number].indexOf(option)
        if (j >= 0) {
            unansweredOptions[number].splice(j, 1);
        }
        if (unansweredOptions[number].length == 0) {
            var i = unanswered.indexOf(number);
            if (i >= 0) {
                unanswered.splice(i, 1);
            }
            delete(unansweredOptions[number])
            return false
        }
    }
    var question = unanswered[0]
    var options = json_data.questions[question]
    if (question in unansweredOptions == false){
        unansweredOptions[question] = options
        $("form").append(newQuestion(question,unansweredOptions[question][0]))
    }
    else{
        changeOption(question,unansweredOptions[question][0])
    }
    var lastInput = $("input.answer").last()
    lastInput.focus()
    lastInput.on("input",checkInputAnswer)
    $("div.option").last()[0].scrollIntoView()
    return true
}