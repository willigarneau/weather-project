
class Color(object):
    tabColor = {-30: '#000099', -20: '#0066ff', -10: '#00ccff', 0: '#00ff00', 10: '#ffcc00', 20: '#ff6600', 30: '#990000'}

    def tempToColor(self, tempC):
        roundTempc = round(tempC, -1)

        #si dépasse extrême
        if(roundTempc < -30):
            roundTempc = -30

        if(roundTempc > 30):
            roundTempc = 30

        for key, value in self.tabColor.items():
            if(key == roundTempc):
                return value

