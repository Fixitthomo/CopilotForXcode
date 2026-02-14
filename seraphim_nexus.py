# Seraphim Nexus

class SeraphimNexus:
    def __init__(self):
        self.data = []

    def add_data(self, item):
        self.data.append(item)

    def display_data(self):
        for item in self.data:
            print(item)

# Example usage
if __name__ == '__main__':
    nexus = SeraphimNexus()
    nexus.add_data('Item 1')
    nexus.add_data('Item 2')
    nexus.display_data()