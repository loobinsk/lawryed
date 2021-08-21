// https://stackoverflow.com/questions/17729194/codemirror-getcursor-not-working-jquery-javascript

function getlist(renderList) {
    // const ul = document.createElement('ul');
    // ul.setAttribute('id', 'proList');

    // let productList = params; // ['products.name', 'products.name2'];


    // document.getElementById('renderList').appendChild(ul);
    // document.getElementById(renderList).appendChild(ul);
    // renderList.appendChild(ul);
    // $("label").attr("for", "id_content").appendChild(ul);
    productList.forEach(renderProductList);

    function renderProductList(element, index, arr) {
        // var li = document.createElement('li');

        // var li = document.createElement('option');
        // // li.setAttribute('class', 'item');
        // li.onclick = ondblclick;
        // ul.appendChild(li);
        // li.innerHTML = li.innerHTML + element;

        const option = document.createElement("option");
        option.value = element;
        option.text = element;
        // option.ondblclick = ondblclick;
        renderList.appendChild(option);
    }
}

function createList() {
    if (productList==null){
        return null;
    }

    const el = $("label").attr("for", "id_content")[2];
    el.appendChild(document.createElement('br'));

    // var renderList=document.createElement('ol');
    const renderList = document.createElement('select');
    renderList.ondblclick = ondblclick;
    renderList.setAttribute("multiple", '');
    renderList.setAttribute("style", 'width: 100%; height: 95%;');
    el.appendChild(renderList);
    getlist(renderList);
}


function ondblclick(event) {
    let value = this.options[this.selectedIndex].value;


    editor.replaceRange(
    // '<div class="gendiv">value</div>\n',  {line: 9,ch: 0}, {line: 9,ch: 0});
    // '<div class="gendiv">{$value}</div>\n', editor.getCursor());
    '{{ '+value+' }}' , editor.getCursor());

    editor.focus();


    //     var area = editor,
    //     curPos = area.prop('selectionEnd');// at the caret **or after selected text**
    //
    // area.val(area.val().substring(0, curPos) + value + area.val().substring(curPos))
    //     .focus()
    //     .prop({'selectionStart': curPos + 1, 'selectionEnd': curPos + 1});
    //

    // https://codemirror.net/doc/manual.html
    // $("textarea").attr("for", "id_content")
    // var w = CodeMirror.fromTextArea($("textarea").attr("for", "id_content"));

}


// $('button.buttonA').click(function () {
//     var area = $('textarea.formInsideMenu'),
//         curPos = area.prop('selectionEnd');// at the caret **or after selected text**
//
//     area.val(area.val().substring(0, curPos) + 'a' + area.val().substring(curPos))
//         .focus()
//         .prop({'selectionStart': curPos + 1, 'selectionEnd': curPos + 1});
// });

createList();


// https://github.com/codemirror/CodeMirror/issues/555
// https://stackoverflow.com/questions/18046144/dynamically-append-div-into-codemirror-without-replacing-initial-code
