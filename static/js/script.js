$(document).ready(function () {
    $('#tables-box').empty()
    get_tables();

})

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

