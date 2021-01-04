$(document).ready(function () {
    $('#tables-box').empty()
    get_tables();
    active_tab()


})

function tab() {
    const tabHeader = document.getElementsByClassName("tab-header")[0];
    const tabIndicator = document.getElementsByClassName("tab-indicator")[0];
    const tabBody = document.getElementsByClassName("tab-body")[0];
    const tabsPane = tabHeader.getElementsByTagName("div");

    for (let i = 0; i < tabsPane.length; i++) {
        tabsPane[i].addEventListener("click", function () {
            tabHeader.getElementsByClassName("active")[0].classList.remove("active");
            tabsPane[i].classList.add("active");

            tabBody.getElementsByClassName("active")[0].classList.remove("active");
            tabBody.getElementsByTagName("div")[i].classList.add("active");

            tabIndicator.style.left = `calc(calc(100%/4)*${i})`
        });

    }
}

function active_tab() {
    $("div.tab-header div").click(function () {
        const tab_id = $(this).attr("data-tab");

        $("div.tab-header div").removeClass('active')
        $(".tab-content").removeClass('active')

        $(this).addClass('active')
        $("#" + tab_id).addClass('active')
    })
    const tabHeader = document.getElementsByClassName("tab-header")[0];
    const tabIndicator = document.getElementsByClassName("tab-indicator")[0];
    const tabsPane = tabHeader.getElementsByTagName("div");

    for (let i = 0; i < tabsPane.length; i++) {
        tabsPane[i].addEventListener("click", function () {
            tabIndicator.style.left = `calc(calc(100%/4)*${i})`
        });

    }
}

function get_tables() {
    $.ajax({
        type: 'GET',
        url: 'api/tables',
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let tables = response['tables']
                for (let i = 0; i < tables.length; i++) {
                    let table = tables[i]

                    makeTable(table['rank'], table['emblem'], table['team_name'], table['played'], table['points'], table['won'], table['draw'], table['lost'], table['gf'], table['ga'], table['gd'])
                }
            }
        }
    })
}

function makeTable(rank, emblem, team_name, played, points, won, draw, lost, gf, ga, gd) {
    let tempHtml = `<tr>
                    <th scope="row">${rank}</th>
                    <td id="tname"><img src="${emblem}" alt="" id="emblem">
                        ${team_name}</td>
                    <td>${played}</td>
                    <td>${points}</td>
                    <td>${won}</td>
                    <td>${draw}</td>
                    <td>${lost}</td>
                    <td>${gf}</td>
                    <td>${ga}</td>
                    <td>${gd}</td>
                  </tr>`
    $('#tables-box').append(tempHtml)

}




