//Update the health of the monster after the attack
function updateHealth(data) {
    var selected_id = ("#monster-id-" + data.user_monster_id);
    var monster_health_left_text = $(selected_id + ' .monster-hp-current');
    monster_health_left_text.text(data.health_left + '');
    var monster_health_bar = $(selected_id + ' .progress-bar');
    monster_health_bar.attr('aria-valuenow', data.health_left + '').css('width', data.percentage + '%');
}

//Respawn a monster
function replaceOldMonster(data, level) {
    var replacedId = "#monster-id-" + data.killed_monster_id;
    var card_name = $(replacedId + ' .card-title');
    card_name.text(data.monster.name);
    var monster_health_left_text = $(replacedId + ' .monster-hp-current');
    monster_health_left_text.text(data.monster.health + '');
    var monster_health_max_text = $(replacedId + ' .monster-hp-max');
    monster_health_max_text.text(data.monster.health + '');
    var monster_health_bar = $(replacedId + " .progress-bar");
    monster_health_bar.attr('aria-valuenow', data.monster.health + '').css('width', '100%');
    monster_health_bar.attr('aria-valuemax', data.monster.health + '').css('width', '100%');
    var image = $(replacedId + " img");
    var d = new Date();
    image.attr('src', data.monster.sprite_url);
    image.attr('alt', data.monster.name);
    var button = $(replacedId + " button");
    var attack_url = '/dashboard/' + data.user_monster_id + '/attack/';
    var funcName = "attackMonster('" + attack_url + "'," + level + ")"; //level should come from server in case it was updated
    button.attr('onclick', funcName);
    $(replacedId).attr('id', 'monster-id-' + data.user_monster_id);
}

//Update player details
function updatePlayer(data) {
    var player_div = "#player-id-" + data.user_profile.id;
    $(player_div + " .player-level").text(data.level);
    $(player_div + " .player-experience").text(data.user_profile.experience);
    $(player_div + " .player-gold").text(data.user_profile.gold);
}

//Write action to the log.
function appendToLog(text, color_class) {
    var d = moment(new Date()).format("HH:mm:ss: ");
    $("#log-list").prepend('<li class="list-group-item list-group-item-action ' + color_class + '">' + d + text + '</li>');
}

//Add new item to user items
function appendToItems(items) {
    items.forEach(function (item) {
        var info = "";
        if (item.item.arm !== 0) {
            info = (" (Arm: " + item.item.arm + ")");
        } else if (item.item.defence !== 0) {
            info = (" (Def: " + item.item.defence + ")")
        } else {
            info = (" (Atk: " + item.item.atk + ")")
        }
        var li_tag = `<li class="list-group-item list-group-item-action list-group-item-primary"><a data-toggle="modal" data-target="#sellModal" data-user-item-id="${item.id}" class="pull-right">Sell </a><p class="d-inline pull-right"> | </p><a href="/dashboard/equip/${item.id}/" class="pull-right">Equip</a>${item.item.name} ${info}</li>`;
        $("#item-list").prepend(li_tag);
    })
}

//Attack monster
function attackMonster(url, level) {
    var extra_data = {level: JSON.stringify(level)};
    $.ajax({
        url: url,
        dataType: "JSON",
        data: extra_data,
        success: function (data) {
            if (data.killed) {
                replaceOldMonster(data, level);
                updatePlayer(data);
                appendToLog(data.damage_message, "list-group-item-danger");
                appendToLog(data.experience_message, "");
                appendToLog(data.loot_message, "list-group-item-warning");
                appendToItems(JSON.parse(data.items));
            } else {
                updateHealth(data, level);
                appendToLog(data.damage_message, "list-group-item-danger");
            }
        },
        error: function () {
            console.log('error');
        }
    });
}

//Sell item
function sellItem(user_item_id) {
    var price = parseInt($('#sellItemPrice').val());
    var url = `/dashboard/sell-item/${user_item_id}/`;
    $.ajax({
        type: "POST",
        url: url,
        data: {'price': price},
        success: function (data) {
            removeItemFromList(data)
        },
        error: function () {
            console.log('error');
        }
    });
}

//Helper that removes item from the list if needed.
function removeItemFromList(data) {
    var item_to_remove = `#item-id-${data.item_to_sell}`;
    $(item_to_remove).remove();
    $("#item-sold-alert").addClass('show');
    $('#sellModal').modal('hide');
}
