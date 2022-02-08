#pragma option -d3

#include <a_samp>
#include "../reverse-proxy.inc"

main()
{
	print("Load Balancer - Test gamemode");
}

public OnPlayerConnect(playerid)
{
    SendClientMessage(playerid, -1, "Type: /ip");
	return 1;
}

public OnPlayerCommandText(playerid, cmdtext[])
{
    if (strcmp(cmdtext, "/ip", true) == 0)
	{
		new proxy_ip[16];
        GetPlayerIp(playerid, proxy_ip, sizeof(proxy_ip));

        new real_ip[16];
        GetPlayerRealIP(playerid, real_ip, sizeof(real_ip));

        new str_text[144];
        format(str_text, sizeof(str_text), "GetPlayerIp = %s, GetPlayerRealIp = %s", proxy_ip, real_ip);
        SendClientMessage(playerid, -1, str_text);
    	return 1;
	}
	return 0;
}

public OnPlayerSpawn(playerid)
{
	return 1;
}

public OnPlayerRequestClass(playerid, classid)
{
	return 1;
}

public OnGameModeInit()
{
	return 1;
}