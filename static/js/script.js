$(document).ready(function () {
    $('#tables-box').empty()
    get_borders();

})

function get_borders() {
    $.ajax({
        type: 'GET',
        url: 'api/borders',
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let epls = response['epls']
                for (let i = 0; i < epls.length; i++) {
                    let epl = epls[i]
                    
                    makeTable(epl['rank'], epl['emblem'], epl['team_name'], epl['played'], epl['points'], epl['won'], epl['draw'], epl['lost'], epl['gf'], epl['ga'], epl['gd'])
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

